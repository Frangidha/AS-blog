from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView
from .models import AboutSection

class AboutView(View):
    model = AboutSection
    template_name = "about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_section = AboutSection.objects.first()
        context['about_section'] = about_section
        return context