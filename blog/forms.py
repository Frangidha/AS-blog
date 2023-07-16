from .models import Review, Post, Category
from django import forms
from django.core.exceptions import ValidationError
from taggit.forms import TagField, TagWidget
from ckeditor.widgets import CKEditorWidget
from cloudinary.forms import CloudinaryFileField


class ReviewForm(forms.ModelForm):
    """Form to create a Review"""

    class Meta:
        model = Review
        fields = ('body', 'methodology_and_experimental_design',
                  'results_and_data_analysis',
                  'discussion_and_interpretation',
                  'contribution_and_originality',
                  'research_objective_and_importance')


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    featured_image = CloudinaryFileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'accept': 'image/jpeg, image/png'})
    )
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    excerpt = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3}), label='Abstract')
    tags = TagField(widget=TagWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('category', 'title', 'excerpt',
                  'content', 'featured_image', 'tags')

    def check_title(self):
        title = self.cleaned_data['title']
        # Check if a post with the same title already exists
        if Post.objects.filter(title=title).exists():
            raise ValidationError('A post with this title already exists.')
        return title
