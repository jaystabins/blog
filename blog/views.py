from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Tag
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostFeedView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = ['-created_at']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_add.html'
    form_class = PostForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostForm

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('article-list')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        obj = Post.objects.get(slug=self.kwargs['slug'])
        return self.request.user.is_superuser or self.request.user.id == obj.user_id


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'blog/tag_add.html'


