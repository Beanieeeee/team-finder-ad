from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("<int:pk>/", views.profile_view, name="profile"),
    path("list/", views.user_list, name="user_list"),
    path("edit/", views.profile_edit, name="profile_edit"),
    path("change-password/", views.change_password, name="change_password"),
    path("edit-profile/", views.profile_edit, name="profile_edit_alt"),
]
