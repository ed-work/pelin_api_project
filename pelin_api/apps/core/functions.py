from django.shortcuts import _get_queryset
import urllib2


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def generate_filename(self, filename):
    filename = urllib2.unquote(filename)
    return "group/%s/%s" % (self.group_id, filename)
