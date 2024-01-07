from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:pk>/', views.Profiles.as_view(), name='profile'),
    path("edit/<slug:pk>/", views.EditProfile.as_view(), name="edit_profile")
]
