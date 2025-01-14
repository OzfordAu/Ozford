from site_settings.models import SiteSettings
from courses.models import HigherEducationCoursePage

def site_settings(request):
    site_settings = SiteSettings.objects.live().public().first()
    courses = HigherEducationCoursePage.objects.live().public()
    pg_courses_data = [
    {
        "title": course.course_title,
        "url": course.get_url()  # Automatically generates the correct relative URL
    }
    for course in courses if course.course_type == 'PG'
]
    ug_courses_data = [
    {
        "title": course.course_title,
        "url": course.get_url()  # Automatically generates the correct relative URL
    }
    for course in courses if course.course_type == 'UG'
]

    if site_settings:
        return {
            'site_settings': site_settings,
            'global_pg_courses': pg_courses_data,
            'global_ug_courses': ug_courses_data,    
        }
    else:
        return {}