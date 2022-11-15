from django.urls import path
from . import views

urlpatterns = [
    path('', views.SongList),
    path('<int:pk>', views.SongDetail)
]