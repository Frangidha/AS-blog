from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    """Form to create a profile"""

    class Meta:
        model = Profile

        fields = ["profile_image", "occupation", "bio_user", "expertises"]

        labels = {"profile_image": "Avatar", "occupation": "Occupation",
                  "bio_user": "Bio", "expertises": "Expertises"}
