from django.conf import settings


def site_info(request):
    """Har template mein `site` variable available karata hai."""
    return {"site": settings.HOSPITAL_INFO}
