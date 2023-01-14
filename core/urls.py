from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import contact

urlpatterns = [
    path("contact", contact, name="contact-form"),
    path("admin/dashboard/", admin.site.index, name="dashboard"),
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path(r"comments/", include("django_comments_xtd.urls")),
    path("accounts/", include("accounts.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
