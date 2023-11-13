from .models import Review, Post, Category, Technique
from django import forms
from django.core.exceptions import ValidationError
from taggit.forms import TagField, TagWidget
from cloudinary.forms import CloudinaryFileField
from django_summernote.widgets import SummernoteWidget


class ReviewForm(forms.ModelForm):
    """Form to create a Review"""

    RATING_CHOICES = (
        (1, 'fundamental'),
        (2, 'Innovative'),
        (3, 'Groundbreaking'),
        (4, 'Insightful'),
        (5, 'Revolutionary'),
    )

    rating = forms.ChoiceField(
        label='Rating',
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        choices=RATING_CHOICES,
        initial=1
    )

    class Meta:
        model = Review
        fields = ('body', 'rating')

# add_post form


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
        widgets = {
            'content': SummernoteWidget(),
        }

    def check_title(self):
        title = self.cleaned_data['title']
        # Check if a post with the same title already exists
        if Post.objects.filter(title=title).exists():
            raise ValidationError('A post with this title already exists.')
        return title
