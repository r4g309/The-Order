from .models import SiteConfig


def site_settings(request):
    defaul_settings = {
        "site_name": "The Order",
    }
    return SiteConfig.objects.first() or defaul_settings
