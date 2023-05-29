from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Category
from .forms import ReviewForm
from taggit.models import Tag
from hitcount.views import HitCountDetailView
from django.db.models import Q
from django.views.generic import DetailView


class CategoryList:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.order_by('title')
        return context
# https://www.codesnail.com/building-a-search-functionality-django-blog-9/


class PostList(CategoryList, generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6
    category_list = Category.objects.order_by('title')
    # search

    def get_queryset(self):
        queryset = super().get_queryset()
        query_search = self.request.GET.get("q")
        if query_search:
            queryset = queryset.filter(
                Q(title__icontains=query_search) |
                Q(tags__name__icontains=query_search)
            ).distinct()
        return queryset


class PostDetail(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = "post_detail.html"

    def get(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        queryset = Post.objects.filter(status=1)
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
                "reviews": reviews,
                "reviewed": False,
                "liked": liked,
                "review_form": ReviewForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        reviews = post.reviews.filter(approved=True).order_by("-created_at")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.author = request.user.username
            review = review_form.save(commit=False)
            review.post = post
            review.save()
        else:
            review_form = ReviewForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "review": review,
                "reviewed": True,
                "review_form": review_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CategoryDetail(CategoryList, generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def category(request, slug):
        category = get_object_or_404(Category, slug=slug)
        posts = category.posts.filter(status=Post.ACTIVE)

        return render(request, 'blog/category.html', {'category': category, 'posts': posts})


class TagFilterView(CategoryList, generic.ListView):
    model = Post
    template_name = 'tags.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        queryset = Post.objects.filter(tags__slug=tag_slug)
        return queryset
