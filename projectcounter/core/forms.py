from django.forms import ModelForm
from models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('created_date',)
