from django.core.paginator import Paginator


PAGE_NUMBER_PARAM = "page"


def paginate_queryset(request, queryset, per_page):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(PAGE_NUMBER_PARAM)
    return paginator.get_page(page_number)
