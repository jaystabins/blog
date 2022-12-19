from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom manager for the Profile model
class ProfileManager(models.Manager):
    def create_profile(self, user):
        profile = self.create(user=user)
        return profile

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(default='media/profile_pics/default.png', upload_to='profile_pics/')
    website_url = models.CharField(max_length=256, blank=True, null=True)
    github_url = models.CharField(max_length=256, blank=True, null=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

# Signal to create a profile for a new user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create_profile(user=instance)
