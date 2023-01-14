from django.urls import path
from .views import PostView, PostFeedView, TagListiew,  upload_image, search

urlpatterns = [
    path('', PostFeedView.as_view(), name='article-list'),
    path('<slug:slug>', PostFeedView.as_view(), name='article-list'),
    path('article/<slug:slug>', PostView.as_view(), name='article-detail'),
    # Tag Management
    path('tags', TagListiew.as_view(), name='tag-list'),
    # Like Post
    path('images/upload_image', upload_image),
    path('search/', search, name='search-post'),
]
