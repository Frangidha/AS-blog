from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post, Category, Review, Technique, Banner
from .forms import ReviewForm, PostForm
from taggit.models import Tag
from hitcount.views import HitCountDetailView
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy


# view to add categories
class CategoryList:
    # add the entire category list to the html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.order_by('title')
        context['selected_category'] = self.kwargs.get('slug')

        return context
# https://www.codesnail.com/building-a-search-functionality-django-blog-9/

class banner:
    # add the entire category list to the html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['switches'] = Banner.objects.all()
        context['selector'] = context['switches'][0].color_display()

        return context

class PostList(banner, CategoryList, generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6
    category_list = Category.objects.order_by('title')
    techniques_list = Technique.objects.order_by('name')
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
    model = Post
    count_hit = True
    template_name = "post_detail.html"

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
                "reviews": reviews,
                "reviewed": False,
                "liked": liked,
                "review_form": ReviewForm(),
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
        review = None
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
                "liked": liked,
            },
        )

# quick way to like post


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

# Search funcionality categories


class CategoryDetail(banner, CategoryList, generic.ListView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return category.posts.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the selected category based on the URL slug
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)

        # Retrieve and add techniques related to the selected category
        techniques = Technique.objects.filter(category=category)

        # Add the category, posts, and techniques to the context
        context['category'] = category
        context['techniques_list'] = techniques

        return context

# Search funcionality based on tags


class TagFilterView(banner, CategoryList, generic.ListView):
    model = Post
    template_name = 'tags.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        queryset = Post.objects.filter(tags__slug=tag_slug, status=1)
        return queryset

# this class allows add their on post


class AddPost(LoginRequiredMixin, View):
    form_class = PostForm
    template_name = 'add_post.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    # post add parameters

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = post.title.replace(" ", "")
            # put at zero so admin can check the post for issues
            post.status = '0'
            post.save()
            # save for the tags
            form.save_m2m()

            messages.success(request, 'Post submitted for approval')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'This title is already in use!')
        return render(request, self.template_name, {'form': form})

# this class allows the user to delete their own review


class DeleteReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a review"""
    model = Review
    success_url = '/'

    def test_func(self):
        return self.request.user.username == self.get_object().author
    # get the succes url of the respective post

    def get_success_url(self):
        post = self.get_object().post
        return reverse('post_detail', kwargs={'slug': post.slug})


# this class allows the user to archive their own post


class ArchivePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Archive a Post"""
    model = Post
    # no field because only 1 button/submit
    fields = []
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        if form.instance.status == 2:
            form.instance.status = 1
        else:
            form.instance.status = 2  # Change the status to 2
        return super().form_valid(form)


class TechniqueList(banner, CategoryList, generic.ListView):
    model = Post  # Change the model to Post
    template_name = 'technique_detail.html'
    context_object_name = 'posts'  # Change the context object name

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        technique_slug = self.kwargs['technique_slug']

        category = get_object_or_404(Category, slug=category_slug)
        technique = get_object_or_404(
            Technique, slug=technique_slug, category=category)

        posts = Post.objects.filter(
            category=category, technique=technique, status=1)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs['category_slug']
        technique_slug = self.kwargs['technique_slug']

        # Retrieve the selected category based on the URL slug
        selected_category = get_object_or_404(Category, slug=category_slug)

        # Retrieve the selected technique based on the URL slug
        selected_technique = get_object_or_404(
            Technique, slug=technique_slug, category=selected_category)

        # Retrieve and add techniques related to the selected category and technique
        techniques = Technique.objects.filter(category=selected_category)

        context['selected_category'] = selected_category
        context['selected_technique'] = selected_technique
        context['techniques_list'] = techniques

        return context