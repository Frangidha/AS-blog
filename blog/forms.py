from .models import Review, Post, Category
from django import forms
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    """Form to create a Review"""
    class Meta:
        model = Review
        fields = ('body', 'methodology_and_experimental_design', 'results_and_data_analysis',
                  'discussion_and_interpretation', 'contribution_and_originality', 'research_objective_and_importance')
        labels = {"methodology_and_experimental_design": "Methodology and Experimental design",
                  "results_and_data_analysis": "Results", "discussion_and_interpretation": "discussion", "contribution_and_originality": "Originality", 'research_objective_and_importance': "Impact"}


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    featured_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={'accept': 'image/jpeg, image/png'}))

    class Meta:
        model = Post
        fields = ('category', 'title','excerpt', 'content', 'featured_image', 'tags')

    def clean_title(self):
        title = self.cleaned_data['title']
        # Check if a post with the same title already exists
        if Post.objects.filter(title=title).exists():
            raise ValidationError('A post with this title already exists.')
        return title
