from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate_queryset

from .forms import ProjectForm
from .models import Project


PROJECTS_PER_PAGE = 12


def get_project_json_response(pk, owner=None):
    projects = Project.objects.all()

    if owner is not None:
        projects = projects.filter(owner=owner)

    project = projects.filter(pk=pk).first()

    if project is None:
        return None, JsonResponse(
            {
                "status": "error",
                "message": "Проект не найден.",
            },
            status=HTTPStatus.NOT_FOUND,
        )

    return project, None


def redirect_to_projects(request):
    return redirect("projects:project_list")


def project_list(request):
    projects = Project.objects.select_related("owner")
    page_obj = paginate_queryset(request, projects, PROJECTS_PER_PAGE)

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

    project.participants.add(project.owner)
    participants = project.participants.exclude(pk=project.owner.pk)

    is_participant = False
    if request.user.is_authenticated:
        is_participant = participants.filter(pk=request.user.pk).exists()

    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "participants": participants,
            "participants_count": participants.count(),
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
    project = get_object_or_404(
        Project.objects.select_related("owner"),
        pk=pk,
        owner=request.user,
    )
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
    project, error_response = get_project_json_response(pk)

    if error_response is not None:
        return error_response

    project.participants.add(project.owner)

    if request.user == project.owner:
        return JsonResponse(
            {
                "status": "error",
                "message": "Автор проекта уже является участником.",
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    is_participant = project.participants.filter(pk=request.user.pk).exists()

    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    participants_count = project.participants.exclude(
        pk=project.owner.pk,
    ).count()

    return JsonResponse(
        {
            "status": "ok",
            "participating": not is_participant,
            "participants_count": participants_count,
        }
    )


@login_required
def complete_project(request, pk):
    project, error_response = get_project_json_response(
        pk,
        owner=request.user,
    )

    if error_response is not None:
        return error_response

    if project.status == Project.STATUS_OPEN:
        project.status = Project.STATUS_CLOSED
        project.save(update_fields=["status"])
        messages.success(request, "Проект завершён.")

    return JsonResponse(
        {
            "status": "ok",
            "project_status": project.status,
        }
    )


@login_required
def toggle_favorite(request, pk):
    project, error_response = get_project_json_response(pk)

    if error_response is not None:
        return error_response

    is_favorited = request.user.favorites.filter(pk=project.pk).exists()

    if is_favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)

    return JsonResponse(
        {
            "status": "ok",
            "favorited": not is_favorited,
        }
    )


@login_required
def favorite_projects(request):
    projects = request.user.favorites.select_related("owner")
    page_obj = paginate_queryset(request, projects, PROJECTS_PER_PAGE)

    return render(
        request,
        "projects/favorite_projects.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
        },
    )
