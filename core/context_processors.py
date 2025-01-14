from site_settings.models import SiteSettings
from courses.models import HigherEducationCoursePage, HighSchoolCoursePage, ElicosCoursePage

def site_settings(request):
    site_settings = SiteSettings.objects.live().public().first()
    courses = HigherEducationCoursePage.objects.live().public()
    high_school_courses = HighSchoolCoursePage.objects.live().public()
    elicos_school_courses = ElicosCoursePage.objects.live().public()
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
    for course in courses if course.course_type == 'UG' or course.course_type == 'DIP'
]

    if site_settings:
        return {
            'site_settings': site_settings,
            'global_pg_courses': pg_courses_data,
            'global_ug_courses': ug_courses_data,    
            'global_high_school_courses': high_school_courses,    
            'global_elicos_school_courses': elicos_school_courses,    
        }
    else:
        return {}