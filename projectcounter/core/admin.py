from django.contrib import admin
from models import Project, Counter


class CounterInline(admin.TabularInline):
    model = Counter
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        CounterInline,
    ]
admin.site.register(Project, ProjectAdmin)
