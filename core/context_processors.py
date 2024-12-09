from site_settings.models import SiteSettings

def site_settings(request):
    site_settings = SiteSettings.objects.live().public().first()
    # print('site', site_settings.header_logo)
    if site_settings:
        return {
            'site_settings': site_settings
        }
    else:
        return {}