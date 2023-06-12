from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Post
from cloudinary.models import CloudinaryField
from django.urls import reverse


class Profile(models.Model):
    """Profile model"""

    user = models.ForeignKey(
        User, related_name="profile", on_delete=models.CASCADE)
    profile_image = CloudinaryField(
        'image',
        transformation=[
            # Set the desired width and height
            {'width': 300, 'height': 300, 'crop': 'fill'}
        ],
        default='xxx', blank=True
    )
    bio_user = RichTextField(max_length=2500, null=True, blank=True)
    occupation = models.CharField(max_length=500, default="N/A")

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.user.id)])


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Create or update the user profile"""
    if created:
        Profile.objects.create(user=instance)
