from django.contrib import admin
from .models import Post, Comment, AnalyticsData


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
            'fields': ('featured_image', 'additional_image')
        }),
        ('Likes', {
            'fields': ('likes',)
        }),
    )


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(AnalyticsData)
