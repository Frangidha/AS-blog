from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    """Form to create a Review"""
    class Meta:
        model = Review
        fields = ('body', 'methodology_and_experimental_design', 'results_and_data_analysis',
                  'discussion_and_interpretation', 'contribution_and_originality', 'research_objective_and_importance')
        labels = {"methodology_and_experimental_design": "Methodology and Experimental design",
                  "results_and_data_analysis": "Results", "discussion_and_interpretation": "discussion", "contribution_and_originality": "Originality", 'research_objective_and_importance': "Impact"}


