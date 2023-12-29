from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health_check', views.health_check, name='health_check'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name='profile'),
    path('settings/<str:template>', views.settings, name='settings'),
    path('settings/', views.settings, name='settings'),
    path('get_design_mode', views.get_design_mode, name='get_design_mode'),
    path('set_design_mode', views.set_design_mode, name='set_design_mode'),
    path('update_personal_info', views.update_personal_info, name='update_personal_info'),
    path('facial_login', views.facial_login, name='facial_login'),
    path('facial_login/enable', views.enable_facial_login, name='enable_facial_login'),
]
