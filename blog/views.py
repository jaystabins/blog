from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Tag
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from core.mixins import SuperuserRequiredMixin

class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostFeedView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = ['-created_at']
    paginate_by = 4
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        context['page_range'] = paginator.page_range[max(0, page_obj.number-3): page_obj.number+2]
        context['tags'] = Tag.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

class PostCreateView(SuperuserRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_add.html'
    form_class = PostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

class PostUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostForm

    def test_func(self):
        obj = Post.objects.get(slug=self.kwargs['slug'])
        return self.request.user.is_superuser or self.request.user.id == obj.user_id

class PostDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('article-list')
    template_name = 'blog/post_confirm_delete.html'

    # Leaving this in for now, if I update the authentication or allow other users to post
    # we can simply remove the SuperuserRequiredMixin
    def test_func(self):
        obj = Post.objects.get(slug=self.kwargs['slug'])
        return self.request.user.is_superuser or self.request.user.id == obj.user_id


class TagCreateView(SuperuserRequiredMixin, CreateView):
    model = Tag
    template_name = 'blog/tag_add.html'
    success_url = reverse_lazy('tag-list')
    fields = ('name',)


class TagListiew(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    ordering = ['-created_at']


@login_required
def LikeView(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(reverse('article-list'))
