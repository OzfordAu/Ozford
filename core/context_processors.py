from site_settings.models import SiteSettings
from courses.models import HigherEducationCoursePage

def site_settings(request):
    site_settings = SiteSettings.objects.live().public().first()
    pg_courses = HigherEducationCoursePage.objects.live().public().filter(course_type='PG')
    pg_courses_data = [
    {
        "title": course.course_title,
        "url": course.get_url()  # Automatically generates the correct relative URL
    }
    for course in pg_courses
]
    ug_courses = HigherEducationCoursePage.objects.live().public().filter(course_type='UG')
    ug_courses_data = [
    {
        "title": course.course_title,
        "url": course.get_url()  # Automatically generates the correct relative URL
    }
    for course in ug_courses
]
    print('pg_courses', pg_courses)
    # print('site', site_settings.header_logo)
    if site_settings:
        return {
            'site_settings': site_settings,
            'global_pg_courses': pg_courses_data,
            'global_ug_courses': ug_courses_data,    
        }
    else:
        return {}