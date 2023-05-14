from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.contrib import admin
from .tag import Tag

STATUS = ((0, "Draft"), (1, "Published"))
#indivual post
class Post(models.Model):
    CATEGORIES = (
        ('microscopy', 'Microscopy'),
        ('vibrational', 'Vibrational'),
        ('nmr', 'NMR'),
        ('thermal', 'Thermal analysis'),
        ('rheology', 'Rheology'),
        ('elemental', 'Elemental analysis'),
        ('gc', 'Gas Chromatography'),
        ('hplc', 'High-Performance Liquid Chromatography'),

    )

    CATEGORY_IMAGES = {
        'microscopy': 'microscopy_default_image.jpg',
        'vibrational': 'vibrational_default_image.jpg',
        'nmr': 'nmr_default_image.jpg',
        'thermal': 'thermal_default_image.jpg',
        'rheology': 'rheology_default_image.jpg',
        'elemental': 'elemental_default_image.jpg',
        'gc': 'gc_default_image.jpg',
        'lc': 'lc_default_image.jpg',
    }

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    additional_image = models.ImageField(upload_to='post_images/', blank=True)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    category = models.CharField(max_length=20, choices=CATEGORIES)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if self.category in self.CATEGORY_IMAGES:
            self.featured_image = self.CATEGORY_IMAGES[self.category]
        super().save(*args, **kwargs)

#user comments
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


#data analytics
class AnalyticsData(models.Model):
    date = models.DateField()
    page_views = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return f"Analytics Data for {self.date}"

admin.site.register(AnalyticsData)