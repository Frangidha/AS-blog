from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from cloudinary.models import CloudinaryField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from blog.models import Category, Technique

# Status choices of the Post
STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Archived'),
)

# Create your models here.
class Mas_event(models.Model):

    category = models.ForeignKey(
        Category, related_name='mas', on_delete=models.CASCADE)
    technique = models.ForeignKey(
        Technique, related_name='mas_technique', on_delete=models.CASCADE, default=None )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_mas")
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
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    event_day = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='mas_like', blank=True)
    tags = TaggableManager()

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    class Meta:
        ordering = ('-event_day',)
    # count the current hits

    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mas_details', args=[self.category.slug, self.slug])
    # set the default images depending on a category

    def save(self, *args, **kwargs):
        if not self.featured_image:
            default_image = self.category.featured_image_default
            if default_image:
                self.featured_image = default_image.url
        super().save(*args, **kwargs)
    # is new banner

    def is_new(self):
        time_difference = timezone.now() - self.created_on
        return time_difference.days <= 7