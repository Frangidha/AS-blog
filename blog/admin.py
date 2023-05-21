from django.contrib import admin
from .models import Post, Review, Profile, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    # Add desired fields for display
    list_display = ('title', 'author', 'created_on', 'status')
    # Add desired fields for filtering
    list_filter = ('created_on', 'status', 'category')
    # Add fields for search functionality
    search_fields = ('title', 'name', 'email', 'body', 'tags__name')
    # Automatically populate the slug field based on the title
    prepopulated_fields = {'slug': ('title',)}
    # action to approve comments on post

    fieldsets = (
        ('Post Details', {
            'fields': ('title', 'slug', 'author', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
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


admin.site.register(Post, PostAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('author', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bio", "image")


admin.site.register(Profile, ProfileAdmin)
