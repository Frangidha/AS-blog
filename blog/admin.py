from django.contrib import admin
from .models import Post, Review, Category, Technique, Banner
from hitcount.models import Hit
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name', 'category__title')  # You can search by name or category title
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate the slug field based on the name

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # Add desired fields for display
    list_display = ('title', 'author', 'created_on',
                    'status')
    # Add desired fields for filtering
    list_filter = ('created_on', 'status', 'category')
    # Add fields for search functionality
    search_fields = ('title', 'name', 'email', 'body', 'tags__name')
    # Automatically populate the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    fieldsets = (
        ('Post Details', {
            'fields': ('title', 'slug', 'author', 'excerpt', 'content')
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('author', 'email', 'body')
    actions = ['approve_reviews']

    def approve_reviewss(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')