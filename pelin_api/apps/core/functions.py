from django.shortcuts import _get_queryset
from multiprocessing import Process
from django.core.mail import EmailMessage
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


def send_password_reset(subject, msg, to, from_email):
    mail = EmailMessage(subject, msg, to=to, from_email=from_email)
    mail.content_subtype = 'html'
    mail.send()


def send_password_reset_async(subject, msg, to, from_email):
    p = Process(target=send_password_reset_async,
                args=[subject, msg, to, from_email])
    p.start()
