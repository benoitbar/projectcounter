from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from forms import ProjectForm
from models import Project, Counter


def home(request):
    projects = Project.objects.all()
    return render_to_response('home.html', {'projects': projects}, context_instance=RequestContext(request))


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    counters = project.counters.all()
    total_days = 0
    total_hours = 0
    user_total_days = {}
    for counter in counters:
        days = counter.get_days()
        hours = counter.get_hours()
        if counter.user.id not in user_total_days:
            user_total_days[counter.user.id] = {'name': counter.user.username, 'days': 0, 'hours': 0}
        user_total_days[counter.user.id]['days'] += days
        user_total_days[counter.user.id]['hours'] += hours
        total_days += days
        total_hours += hours
    is_started = False
    if request.user.is_authenticated():
        try:
            counters.get(user=request.user, end_date__isnull=True)
            is_started = True
        except Counter.DoesNotExist:
            pass
    return render_to_response('project.html', {'project': project, 'is_started': is_started, 'counters': counters, 'total_days': total_days, 'user_total_days': user_total_days, 'total_hours': total_hours}, context_instance=RequestContext(request))


@login_required
def start(request, id):
    project = get_object_or_404(Project, pk=id)
    Counter.objects.start(request.user, project)
    return redirect('project', id)


@login_required
def stop(request, id):
    project = get_object_or_404(Project, pk=id)
    Counter.objects.stop(request.user, project)
    return redirect('project', id)


def toggle(request, project_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    project = get_object_or_404(Project, pk=project_id)
    if Counter.objects.stop(user=user, project=project) is None:
        Counter.objects.start(user=user, project=project)
    return render_to_response('close.html', {})


def add(request):
    if request.method == 'POST':
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render_to_response('add.html', {'form': form}, context_instance=RequestContext(request))
