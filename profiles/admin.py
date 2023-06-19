from django.contrib import admin
from .models import Profile, Expertise


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bio_user")


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    pass
