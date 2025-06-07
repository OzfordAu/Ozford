from datetime import date
from site_settings.models import SiteSettings
from courses.models import HigherEducationCoursePage, HighSchoolCoursePage, ElicosCoursePage

def site_settings(request):
    today = date.today()
    site_settings = SiteSettings.objects.live().public().first()
    courses = HigherEducationCoursePage.objects.live().public()
    high_school_courses = HighSchoolCoursePage.objects.live().public()
    elicos_school_courses = ElicosCoursePage.objects.live().public()

    pg_courses_data = [
        {
            "title": course.course_title,
            "url": course.get_url()
        }
        for course in courses if course.course_type == 'PG'
    ]

    ug_courses_data = [
        {
            "title": course.course_title,
            "url": course.get_url()
        }
        for course in courses if course.course_type in ['UG', 'DIP']
    ]

    # Determine if popup should show
    show_popup = False
    if site_settings and site_settings.popup_is_active:
        if (not site_settings.popup_start_date or site_settings.popup_start_date <= today) and \
           (not site_settings.popup_end_date or site_settings.popup_end_date >= today):
            show_popup = True

    return {
        'site_settings': site_settings,
        'global_pg_courses': pg_courses_data,
        'global_ug_courses': ug_courses_data,
        'global_high_school_courses': high_school_courses,
        'global_elicos_school_courses': elicos_school_courses,
        'show_popup': show_popup,
    }
