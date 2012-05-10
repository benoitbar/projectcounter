from django.conf.urls import patterns, url


urlpatterns = patterns('projectcounter.core',
    url(r'^$', 'views.home', name='home'),
    url(r'^project/(?P<id>\d+)/$', 'views.project', name='project'),
    url(r'^start/(?P<id>\d+)/$', 'views.start', name='start'),
    url(r'^stop/(?P<id>\d+)/$', 'views.stop', name='stop'),
    url(r'^toggle/(?P<user_id>\d+)/(?P<project_id>\d+)/$', 'views.toggle', name='toggle'),
    url(r'^add/$', 'views.add', name='add'),
)
