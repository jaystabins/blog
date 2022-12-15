from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import PostView, PostFeedView, PostCreateView, PostUpdateView, PostDeleteView, TagCreateView

urlpatterns = [
    path('', PostFeedView.as_view(), name='article-list'),
    path('article/createarticle', PostCreateView.as_view(), name='article-create'),
    path('article/createtag', TagCreateView.as_view(), name='tag-create'),
    path('article/<str:slug>', PostView.as_view(), name='article-detail'),
    path('article/<str:slug>/updatearticle', PostUpdateView.as_view(), name='article-update'),
    path('article/<str:slug>/deletearticle', PostDeleteView.as_view(), name='article-delete'),
]
