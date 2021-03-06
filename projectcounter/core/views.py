from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from forms import ProjectForm, CounterForm
from models import Project, Counter
from django.http import HttpResponse, HttpResponseNotModified, HttpResponseForbidden, HttpResponseNotFound
from datetime import timedelta


def home(request):
    projects = Project.objects.all()
    return render_to_response('home.html', {'projects': projects}, context_instance=RequestContext(request))


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    counters = project.counters.all()
    total_days = timedelta(0)
    user_total_days = {}
    for counter in counters:
        days = counter.get_timedelta()
        if counter.user.id not in user_total_days:
            user_total_days[counter.user.id] = {'name': counter.user.username, 'days': timedelta(0)}
        user_total_days[counter.user.id]['days'] += days
        total_days += days
    is_started = False
    if request.user.is_authenticated():
        try:
            counters.get(user=request.user, end_date__isnull=True)
            is_started = True
        except Counter.DoesNotExist:
            pass
    return render_to_response('project.html', {'project': project, 'is_started': is_started, 'counters': counters, 'total_days': total_days, 'user_total_days': user_total_days}, context_instance=RequestContext(request))


@login_required
def start(request, id):
    project = get_object_or_404(Project, pk=id)
    Counter.objects.start(request.user, project)
    return redirect('core:project', id)


@login_required
def stop(request, id):
    project = get_object_or_404(Project, pk=id)
    Counter.objects.stop(request.user, project)
    return redirect('core:project', id)


def toggle(request, project_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    project = get_object_or_404(Project, pk=project_id)
    if Counter.objects.stop(user=user, project=project) is None:
        Counter.objects.start(user=user, project=project)
    return render_to_response('close.html', {})


@login_required
def add(request):
    if request.method == 'POST':
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = ProjectForm()
    return render_to_response('add.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def edit(request, counter_id):
    if request.method == 'POST':
        try:
            counter = Counter.objects.get(pk=counter_id)
            form = CounterForm(data=request.POST, instance=counter)
            if form.is_valid():
                form.save()
                counters = counter.project.counters.all()
                total_days = timedelta(0)
                user_total_days = {}
                for counter in counters:
                    days = counter.get_timedelta()
                    if counter.user.id not in user_total_days:
                        user_total_days[counter.user.id] = {'name': counter.user.username, 'days': timedelta(0)}
                    user_total_days[counter.user.id]['days'] += days
                    total_days += days
                return render_to_response('project.ajax.html', {'counters': counters, 'total_days': total_days, 'user_total_days': user_total_days}, context_instance=RequestContext(request))
            else:
                from django.utils import simplejson as json
                return HttpResponse(json.dumps(form.errors), content_type='application/json', status=304)   # Not Modified
        except Counter.DoesNotExist():
            return HttpResponseNotFound
    else:
        return HttpResponseForbidden()
