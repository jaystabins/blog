from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Tag
from django.db.models import Q

# TinyMCE Image Uplaod Imports
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import PostImage
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

class PostView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostFeedView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    ordering = ['-created_at']
    paginate_by = 200
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
        queryset = queryset.filter(is_published=True)

        return queryset


class TagListiew(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    ordering = ['-created_at']

@user_passes_test(lambda u: u.is_superuser)
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        image = Image.open(io.BytesIO(file_obj.read()))

        image.thumbnail((500,500))

        resized_image = io.BytesIO()
        image.save(resized_image, format=image.format)

        django_file = InMemoryUploadedFile(resized_image, None, file_obj.name, file_obj.content_type, resized_image.tell, None)
        try:
            img = PostImage(image=django_file)
            img.save()
        except Exception:
            return JsonResponse({'message': 'Problem Saving The Image'})

        return JsonResponse({
            'message': 'Image uploaded successfully',
            # 'location': file_url
            'location': img.image.url
        })
    return JsonResponse({'detail': "Wrong request"})

def search(request):
    query = request.POST.get('q')
    tags = Tag.objects.all()
    if query:
        object_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(tagline__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__icontains=query)
        )
    else:
        object_list = None
    return render(request, 'blog/post_list.html', {'object_list': object_list, 'tags': tags})