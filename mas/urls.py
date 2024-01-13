from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.MasList.as_view(), name='mas'),
    path('<slug:slug>/', views.MasDetail.as_view(), name='mas_detail'),
    path('like/<slug:slug>/', views.MasLike.as_view(), name='mas_like'),
]
