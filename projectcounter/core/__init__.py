from django.conf import settings


settings.HOURS_BY_DAY = getattr(settings, 'HOURS_BY_DAY', 7)
