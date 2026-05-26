from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate_queryset

from .forms import LoginForm, ProfileEditForm, RegisterForm
from .models import User


USERS_PER_PAGE = 12

FILTER_OWNERS_OF_FAVORITE_PROJECTS = "owners-of-favorite-projects"
FILTER_OWNERS_OF_PARTICIPATING_PROJECTS = "owners-of-participating-projects"
FILTER_INTERESTED_IN_MY_PROJECTS = "interested-in-my-projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS = "participants-of-my-projects"


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Аккаунт успешно создан. Теперь войдите в систему.")
        return redirect("users:login")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        login(request, form.cleaned_data["user"])
        messages.success(request, "Вы вошли в аккаунт.")
        return redirect("projects:project_list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect("projects:project_list")


def profile_view(request, pk):
    user = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        pk=pk,
    )

    return render(
        request,
        "users/user-details.html",
        {
            "user": user,
        },
    )


def user_list(request):
    users = User.objects.prefetch_related(
        "owned_projects",
        "participated_projects",
        "favorites",
    ).order_by("-id")

    active_filter = request.GET.get("filter")

    if request.user.is_authenticated and active_filter:
        if active_filter == FILTER_OWNERS_OF_FAVORITE_PROJECTS:
            users = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct()

        elif active_filter == FILTER_OWNERS_OF_PARTICIPATING_PROJECTS:
            users = User.objects.filter(
                owned_projects__participants=request.user
            ).distinct()

        elif active_filter == FILTER_INTERESTED_IN_MY_PROJECTS:
            users = User.objects.filter(
                favorites__owner=request.user
            ).distinct()

        elif active_filter == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
            users = User.objects.filter(
                participated_projects__owner=request.user
            ).exclude(pk=request.user.pk).distinct()

    page_obj = paginate_queryset(request, users, USERS_PER_PAGE)

    query_prefix = ""
    if active_filter:
        query_prefix = f"filter={active_filter}&"

    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "page_obj": page_obj,
            "active_filter": active_filter,
            "query_prefix": query_prefix,
        },
    )


@login_required
def profile_edit(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Профиль успешно обновлён.")
        return redirect("users:profile", pk=request.user.pk)

    return render(
        request,
        "users/edit_profile.html",
        {
            "form": form,
        },
    )


@login_required
def change_password(request):
    form = PasswordChangeForm(
        user=request.user,
        data=request.POST or None,
    )

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль успешно изменён.")
        return redirect("users:profile", pk=request.user.pk)

    return render(
        request,
        "users/change_password.html",
        {
            "form": form,
        },
    )
