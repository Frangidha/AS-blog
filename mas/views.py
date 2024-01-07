from django.shortcuts import render

# Create your views here.
class MasList(banner, generic.ListView):
    model = Mas_event
    queryset = Mas.objects.filter(status=1).order_by("-created_on")
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


# post Detail html(hitcountview for tracking of views)


class PostDetail(HitCountDetailView):
    model = Mas_event
    count_hit = True
    template_name = "mas_detail.html"

    def get(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        queryset = Post.objects.filter(status__in=[0, 1, 2])
        post = get_object_or_404(queryset, slug=slug)
        reviews = post.reviews.filter(approved=True).order_by("-created_at")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "liked": liked,
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        reviews = post.reviews.filter(approved=True).order_by("-created_at")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True


        return render(
            request,
            "mas_detail.html",
            {
                "mas_event": 'event_day',
                "liked": liked,
            },
        )
