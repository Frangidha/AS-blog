from . import views
from django.urls import path, include

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('', views.PostList.as_view(), name='home'),
    path('add_post/', views.AddPost.as_view(), name='add_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('category/<slug:slug>/',
         views.CategoryDetail.as_view(), name='category_detail'),
    path('tag/<slug:tag_slug>/',
         views.TagFilterView.as_view(), name='tag_filter'),
    path('profiles/', include('profiles.urls')),
    path('review/<int:pk>/delete/',
         views.DeleteReview.as_view(), name='delete_review'),
    path('post/<int:pk>/archive/',
         views.ArchivePost.as_view(), name='archive_post'),
    path('category/<slug:category_slug>/<slug:technique_slug>/',
         views.TechniqueList.as_view(), name='technique_detail'),
]
