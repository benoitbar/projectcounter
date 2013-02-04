from django.conf import settings


settings.HOURS_BY_DAY = getattr(settings, 'HOURS_BY_DAY', 7)
settings.DAY_BY_WEEK = getattr(settings, 'DAY_BY_WEEK', 5)
settings.DAY_BY_MONTH = getattr(settings, 'DAY_BY_MONTH', 20)
settings.DAY_BY_YEAR = getattr(settings, 'DAY_BY_YEAR', 240)
