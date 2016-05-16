from multiprocessing import Process

from pusher import Pusher
from django.conf import settings


pusher = Pusher(
    app_id=settings.PUSHER['APP_ID'],
    key=settings.PUSHER['KEY'],
    secret=settings.PUSHER['SECRET'])


def pusher_async(channel, event, data):
    p = Process(target=pusher.trigger, args=(channel, event, data))
    p.start()

# TODO: send notification to pusher
# TODO: send notification to GCM

# TODO: pusher function wrapper with multiprocess
# TODO: GCM function wrapper with multiprocess
