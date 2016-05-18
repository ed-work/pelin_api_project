from multiprocessing import Process

from pusher import Pusher
from django.conf import settings


pusher = Pusher(
    app_id=settings.PUSHER['APP_ID'],
    key=settings.PUSHER['KEY'],
    secret=settings.PUSHER['SECRET'])


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def pusher_async(channel, event, data):
    if isinstance(channel, list):
        chunked_channels = chunks(channel, 10)
        for channels in chunked_channels:
            p = Process(target=pusher.trigger, args=(channels, event, data))
            p.start()
    else:
        p = Process(target=pusher.trigger, args=(channel, event, data))
        p.start()

# TODO: send notification to pusher
# TODO: send notification to GCM

# TODO: pusher function wrapper with multiprocess
# TODO: GCM function wrapper with multiprocess
