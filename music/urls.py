from django.urls import path
from . import views

urlpatterns = [
    path('', views.song_list),
    path('<int:pk>/', views.song_detail),
    path('song_like/<int:pk>', views.song_like)
]