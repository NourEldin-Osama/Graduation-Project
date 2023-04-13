from django.urls import path

from apps.video_generation import views

urlpatterns = [
    path('video_generation', views.video_generation, name='video_generation'),
    path('video_generation_api', views.video_generation_api, name='video_generation_api'),
]
