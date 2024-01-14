from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from blog.models import Category, Technique
from .models import Mas_event
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from hitcount.views import HitCountDetailView
# MAS annoucement List
class MasList(generic.ListView):
    model = Mas_event
    queryset = Mas_event.objects.filter(status=1).order_by("-event_day")
    template_name = "mas.html"
    paginate_by = 3
    # search
    # https://www.youtube.com/watch?v=cP4HKyqNQsw&ab_channel=BLearningClub
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query_search = self.request.GET.get("q")
        if query_search:
            queryset = queryset.filter(
                Q(title__icontains=query_search) |
                Q(tags__name__icontains=query_search)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mas_list'] = context['mas_event_list']
        return context

# MAS Detail html(hitcountview for tracking of views) - Not activated

class MasDetail(HitCountDetailView):
    model = Mas_event
    template_name = "mas_detail.html"

    def get(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        queryset = Mas_event.objects.filter(status__in=[0, 1, 2])
        mas = get_object_or_404(queryset, slug=slug)
        liked = False
        if self.object.likes.filter(id=request.user.id).exists():
            liked = True

        context["liked"] = liked


        return render(
            request,
            "mas_detail.html",
            {
                "mas": mas,
                "liked": liked,
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Mas_event.objects.filter(status=1)
        mas = get_object_or_404(queryset, slug=slug)
        liked = False
        if mas.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "mas_detail.html",
            {
                "mas": mas,
                "liked": liked,
            },
        )

class MasLike(View):
    def post(self, request, slug, *args, **kwargs):
        mas = get_object_or_404(Mas_event, slug=slug)
        
        if mas.likes.filter(id=request.user.id).exists():
            mas.likes.remove(request.user)
        else:
            mas.likes.add(request.user)

        return HttpResponseRedirect(reverse('mas_detail', args=[mas.slug]))