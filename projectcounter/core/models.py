from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)


class Project(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return smart_str(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)

    def get_absolute_url(self):
        return '/project/%s/' % self.id


class CounterManager(models.Manager):
    def start(self, user, project):
        self.stop(user, project)
        Counter(user=user, project=project, start_date=datetime.now()).save()

    def stop(self, user, project):
        try:
            counter = self.get(user=user, project=project, end_date=None)
            counter.end_date = datetime.now()
            counter.save()
            return counter
        except self.model.DoesNotExist:
            return None


class Counter(models.Model):
    project = models.ForeignKey(Project, related_name='counters')
    user = models.ForeignKey(User, related_name='counters')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    objects = CounterManager()

    def is_started(self):
        return self.end_date is not None

    def get_timedelta(self):
        if self.end_date is None:
            return timedelta(0)
        td = self.end_date - self.start_date
        return td

    class Meta:
        ordering = ['start_date']
        get_latest_by = "start_date"

    def __unicode__(self):
        return smart_unicode(self.project.name)
