from django.conf import settings


def settings_context(_request):
    return {
        "PROJECT_TITLE": settings.PROJECT_TITLE,
        "COPYRIGHT": settings.COPYRIGHT,
        "META_URL": settings.META_URL,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "AWS_IMAGE_URL": settings.AWS_IMAGE_URL,
    }
