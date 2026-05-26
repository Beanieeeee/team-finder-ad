from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import LoginForm, ProfileEditForm, RegisterForm
from django.contrib.auth import update_session_auth_hash
from .models import User

from .forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileEditForm,
    RegisterForm,
)


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
    users = User.objects.all().order_by("-id")

    active_filter = request.GET.get("filter")

    if request.user.is_authenticated and active_filter:

        if active_filter == "favorite_authors":
            users = User.objects.filter(
                owned_projects__in=request.user.favorites.all()
            ).distinct()

        elif active_filter == "participated_authors":
            users = User.objects.filter(
                owned_projects__participants=request.user
            ).distinct()

        elif active_filter == "liked_my_projects":
            users = User.objects.filter(
                favorites__owner=request.user
            ).distinct()

        elif active_filter == "participants_my_projects":
            users = User.objects.filter(
                participated_projects__owner=request.user
            ).exclude(pk=request.user.pk).distinct()

    paginator = Paginator(users, 12)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "page_obj": page_obj,
            "active_filter": active_filter,
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
    form = CustomPasswordChangeForm(
        user=request.user,
        data=request.POST or None,
    )

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Аккаунт успешно создан. Теперь войдите в систему.")
        messages.success(request, "Аккаунт успешно создан. Теперь войдите в систему.")
        messages.success(request, "Вы вошли в аккаунт.")
        messages.success(request, "Вы вышли из аккаунта.")
        messages.success(request, "Профиль успешно обновлён.")
        messages.success(request, "Пароль успешно изменён.")
        return redirect("users:profile", pk=request.user.pk)

    return render(
        request,
        "users/change_password.html",
        {
            "form": form,
        },
    )