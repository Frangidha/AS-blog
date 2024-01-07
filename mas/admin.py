from django.contrib import admin
from blog.models import Category, Technique
from .models import Mas_event
from hitcount.models import Hit
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Mas_event)
class PostAdmin(SummernoteModelAdmin):
    # Add desired fields for display
    list_display = ('title', 'author','event_day', 'created_on',
                    'status')
    # Add desired fields for filtering
    list_filter = ('created_on', 'status', 'category')
    # Add fields for search functionality
    search_fields = ('title', 'name', 'email', 'body', 'tags__name')
    # Automatically populate the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    fieldsets = (
        ('Mas_detail', {
            'fields': ('title', 'slug', 'author', 'event_day','excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category','technique','tags')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Images', {
            'fields': ('featured_image',)
        }),
        ('Likes', {
            'fields': ('likes',)
        }),

    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_prepopulated_fields(self, request, obj=None):
        prepopulated_fields = super().get_prepopulated_fields(request, obj)
        if obj and 'category' in prepopulated_fields.get('tags', ()):
            category_title = obj.category.title
            prepopulated_fields['tags'] = ('category__title',)
            prepopulated_fields['tags_overrides'] = {
                'category__title': category_title}
        return prepopulated_fields