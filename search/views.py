from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db.models import Q
from wagtail.models import Page
from courses.models import HighSchoolCoursePage, HigherEducationCoursePage, ElicosCoursePage


def _normalize(page, request, title=None, description=None):
    return {
        "title": title or getattr(page, "title", ""),
        "description": description or getattr(page, "search_description", "") or "",
        "url": page.get_url(request),
    }


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    search_results = []

    if search_query:
        seen_ids = set()

        # Course pages first, with their richer descriptions
        higher_ed_results = HigherEducationCoursePage.objects.live().filter(
            Q(course_title__icontains=search_query) |
            Q(course_header_description__icontains=search_query)
        )
        high_school_results = HighSchoolCoursePage.objects.live().filter(
            Q(course_title__icontains=search_query) |
            Q(course_header_description__icontains=search_query)
        )
        elicos_results = ElicosCoursePage.objects.live().filter(
            Q(course_title__icontains=search_query) |
            Q(course_header_description__icontains=search_query)
        )

        for course_page in list(higher_ed_results) + list(high_school_results) + list(elicos_results):
            seen_ids.add(course_page.id)
            search_results.append(_normalize(
                course_page,
                request,
                title=course_page.course_title,
                description=course_page.course_header_description,
            ))

        # Every other live page on the site — Fees, How to Apply, About, etc.
        general_pages = Page.objects.live().search(search_query)
        for result in general_pages:
            specific_page = result.specific
            if specific_page.id in seen_ids:
                continue
            seen_ids.add(specific_page.id)
            search_results.append(_normalize(specific_page, request))

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
