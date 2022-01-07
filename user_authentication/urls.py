from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register_user, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('destroy_user/<int:id>', views.destroy_user, name="destroy_user"),
    path('users/new', views.new_user, name="new_user"),
    path('users/<int:id>/edit', views.edit, name="edit_user"),
    path('users/<int:id>/update', views.update, name="update_user"),
    path('passwords/new', views.forgot_password, name="forgot_password"),
    path('passwords/update', views.new_passwords, name="update_password"),
]
