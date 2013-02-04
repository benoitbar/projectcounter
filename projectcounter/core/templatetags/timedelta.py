from django import template
from django.conf import settings
from django.template.base import Library
from django.utils.translation import ugettext, ungettext
from datetime import datetime


register = Library()


def timesince(d, now=datetime.now(), timedelta=False):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes". If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored. Up to two adjacent units will be
    displayed. For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
    """
    if now is None:
        return ''

    chunks = (
      (60 * 60 * settings.HOURS_BY_DAY * settings.DAY_BY_YEAR, lambda n: ungettext('year', 'years', n)),
      (60 * 60 * settings.HOURS_BY_DAY * settings.DAY_BY_MONTH, lambda n: ungettext('month', 'months', n)),
      (60 * 60 * settings.HOURS_BY_DAY * settings.DAY_BY_WEEK, lambda n: ungettext('week', 'weeks', n)),
      (60 * 60 * settings.HOURS_BY_DAY, lambda n: ungettext('day', 'days', n)),
      (60 * 60, lambda n: ungettext('hour', 'hours', n)),
      (60, lambda n: ungettext('minute', 'minutes', n))
    )

    if timedelta:
        delta = d
    else:
        delta = now - d
    # ignore microseconds
    since = delta.days * settings.HOURS_BY_DAY * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return '0 ' + ugettext('minutes')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += ugettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
    return s


@register.tag(name="timedelta")
def do_timedelta(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, start_date, end_date = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    return TimedeltaNode(start_date, end_date)


class TimedeltaNode(template.Node):
    def __init__(self, start_date, end_date):
        self.start_date = template.Variable(start_date)
        self.end_date = template.Variable(end_date)

    def render(self, context):
        try:
            start_date = self.start_date.resolve(context)
            end_date = self.end_date.resolve(context)
            return timesince(start_date, end_date)
        except template.VariableDoesNotExist:
            return ''


@register.filter(name="timedelta")
def timedelta(value):
    return timesince(value, timedelta=True)
