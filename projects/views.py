from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


def redirect_to_projects(request):
    return redirect("projects:project_list")


def project_list(request):
    projects = Project.objects.select_related("owner").all()
    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=pk,
    )

    is_participant = False
    if request.user.is_authenticated:
        is_participant = project.participants.filter(pk=request.user.pk).exists()

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "is_participant": is_participant,
        },
    )


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        messages.success(request, "Проект успешно создан.")
        return redirect("projects:project_detail", pk=project.pk)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        project = form.save()
        messages.success(request, "Проект успешно обновлён.")
        return redirect("projects:project_detail", pk=project.pk)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": True,
        },
    )


@login_required
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user == project.owner:
        return JsonResponse({"status": "error"}, status=400)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        participating = False
    else:
        project.participants.add(request.user)
        participating = True

    return JsonResponse({
        "status": "ok",
        "participating": participating,
    })


@login_required
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if project.status == Project.STATUS_OPEN:
        project.status = Project.STATUS_CLOSED
        project.save(update_fields=["status"])
        messages.success(request, "Проект завершён.")

    return JsonResponse({
        "status": "ok",
        "project_status": project.status,
    })


@login_required
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse({
        "status": "ok",
        "favorited": favorited,
    })


@login_required
def favorite_projects(request):
    projects = request.user.favorites.all()

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/favorite_projects.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
        },
    )