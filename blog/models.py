from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from tinymce import models as tinymce_models


class Tag(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=255, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("article-list")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=255, null=False, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = tinymce_models.HTMLField()
    tagline = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(
        upload_to="articles/", default="../static/img/smokeymtn.jpg"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    is_published = models.BooleanField(default=False)
    allow_comments = models.BooleanField("allow comments", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " | " + str(self.author)

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PostImage(models.Model):
    image = models.ImageField(upload_to="articles/content/")
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"
