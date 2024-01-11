from django.contrib import admin
from .models import AboutSection
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(AboutSection)
class PostAdmin(SummernoteModelAdmin):
    # Automatically populate the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    fieldsets = (
        ('About', {
            'fields': ('title', 'slug', 'author', 'content')
        }),
    )