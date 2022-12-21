from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import contact

urlpatterns = [
    path('contact', contact, name='contact-form'),
    path('admin/dashboard/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include("accounts.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)