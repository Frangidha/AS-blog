from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    """Form to create a profile"""

    class Meta:
        model = Profile
        fields = ["profile_image", "bio_user"]

        labels = {"profile_image": "Avatar", "bio_user": "Bio"}
