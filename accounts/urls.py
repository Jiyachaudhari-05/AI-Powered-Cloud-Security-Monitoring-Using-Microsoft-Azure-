from django.urls import path
from . import views
from .views import send_email
from . import views


urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('register/', views.register_user, name='register'),

    
]