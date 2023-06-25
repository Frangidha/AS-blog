import os
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.auth.models import User
from django.db.models.signals import post_save


STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Archived'),
)
# https://github.com/SteinOveHelset/crashblog


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    featured_image_default = CloudinaryField('image',
                                             transformation=[
                                                 # Set the desired width and height
                                                 {'width': 400, 'height': 200,
                                                     'crop': 'fill'}
                                             ], blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-detail', args=[self.slug])


class Post(models.Model):

    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField(
        'image',
        transformation=[
            # Set the desired width and height
            {'width': 400, 'height': 200, 'crop': 'fill'}
        ],
        default='', blank=True
    )
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)
    tags = TaggableManager()

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    class Meta:
        ordering = ('-created_on',)

    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        if not self.featured_image:
            default_image = self.category.featured_image_default
            if default_image:
                self.featured_image = default_image.url
        super().save(*args, **kwargs)


class Review(models.Model):

    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    post = models.ForeignKey(
        Post, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    research_objective_and_importance = models.PositiveIntegerField(
        null=True, choices=RATINGS)
    methodology_and_experimental_design = models.PositiveIntegerField(
        null=True, choices=RATINGS)
    results_and_data_analysis = models.PositiveIntegerField(
        null=True, choices=RATINGS)
    discussion_and_interpretation = models.PositiveIntegerField(
        null=True, choices=RATINGS)
    contribution_and_originality = models.PositiveIntegerField(
        null=True, choices=RATINGS)

    approved = models.BooleanField(default=False)


def __str__(self):
    return self.author
