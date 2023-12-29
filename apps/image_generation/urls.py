from django.urls import path

from apps.image_generation import views

urlpatterns = [
    path('image_generation', views.image_generation, name='image_generation'),
    path('generate_image', views.generate_image_api, name='generate_image'),
    path('get_status_image', views.get_status_api, name='get_status_image'),
    path('get_image', views.get_image_api, name='get_image'),
]
