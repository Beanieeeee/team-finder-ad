from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.redirect_to_projects, name="index"),

    path(
        "projects/list/",
        views.project_list,
        name="project_list",
    ),

    path(
        "projects/create-project/",
        views.project_create,
        name="project_create",
    ),

    path(
        "projects/<int:pk>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
        "projects/<int:pk>/edit/",
        views.project_edit,
        name="project_edit",
    ),

    path(
        "projects/<int:pk>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),

    path(
        "projects/<int:pk>/toggle-participate",
        views.toggle_participate,
        name="toggle_participate_no_slash",
    ),

    path(
        "projects/<int:pk>/complete/",
        views.complete_project,
        name="complete_project",
    ),

    path(
        "projects/<int:pk>/complete",
        views.complete_project,
        name="complete_project_no_slash",
    ),

    path(
        "projects/<int:pk>/toggle-favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),

    path(
        "projects/<int:pk>/toggle-favorite",
        views.toggle_favorite,
        name="toggle_favorite_no_slash",
    ),

    path(
        "projects/favorites/",
        views.favorite_projects,
        name="favorite_projects",
    ),
]
