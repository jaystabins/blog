from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import PostView, PostFeedView, PostCreateView, PostUpdateView, PostDeleteView, TagCreateView, TagListiew, LikeView

urlpatterns = [
    path('articles/', PostFeedView.as_view(), name='article-list'),
    path('articles/<slug:slug>', PostFeedView.as_view(), name='article-list'),
    path('article/createarticle', PostCreateView.as_view(), name='article-create'),
    path('article/<slug:slug>', PostView.as_view(), name='article-detail'),
    path('article/<slug:slug>/updatearticle', PostUpdateView.as_view(), name='article-update'),
    path('article/<slug:slug>/deletearticle', PostDeleteView.as_view(), name='article-delete'),
    # Tag Management
    path('tags', TagListiew.as_view(), name='tag-list'),
    path('tags/createtag', TagCreateView.as_view(), name='tag-create'),
    # Like Post
    path('like/<slug:slug>', LikeView, name='article-like'),
]
