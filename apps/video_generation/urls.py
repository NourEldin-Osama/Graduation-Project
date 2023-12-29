from django.urls import path

from apps.video_generation import views

urlpatterns = [
    path('video_generation', views.video_generation, name='video_generation'),
    path('transform_character', views.transform_character_api, name='transform_character'),
    path('get_status_video', views.get_status_api, name='get_status_video'),
    path('get_video', views.get_video_api, name='get_video'),
    path('add_character', views.add_character, name='add_character'),
]
