from django.forms import ModelForm
from models import Project, Counter


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('created_date',)


class CounterForm(ModelForm):
    class Meta:
        model = Counter
        exclude = ('project', 'user',)
