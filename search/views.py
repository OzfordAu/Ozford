from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db.models import Q
from courses.models import HighSchoolCoursePage, HigherEducationCoursePage, ElicosCoursePage

def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    if search_query:
        # Search across all course types
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

        # Combine all results
        search_results = list(higher_ed_results) + list(high_school_results) + list(elicos_results)
    else:
        search_results = []

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
