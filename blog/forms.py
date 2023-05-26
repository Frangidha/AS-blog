from .models import Review, Profile
from django import forms


class ReviewForm(forms.ModelForm):
    """Form to create a Review"""
    class Meta:
        model = Review
        fields = ('body', 'methodology_and_experimental_design', 'results_and_data_analysis',
                  'discussion_and_interpretation', 'contribution_and_originality')
        labels = {"methodology_and_experimental_design": "Methodology and Experimental design",
                  "results_and_data_analysis": "Results", "discussion_and_interpretation": "discussion", "contribution_and_originality": "Originality"}


class ProfileForm(forms.ModelForm):
    """Form to create a profile"""

    class Meta:
        model = Profile
        fields = ["image", "bio"]

        labels = {"image": "Avatar", "bio": "Bio"}
