import requests
from multiprocessing import Process

from pusher import Pusher
from django.conf import settings

HEADERS = {
    'content-type': 'application/json',
    'authorization': 'key=' + settings.FCM_SERVER_ID
}

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


def fcm(register_ids, data):
    data = {
        'notification': data,
        'registration_ids': register_ids,
    }
    requests.post(settings.FCM_URL, data=data, headers=HEADERS)


def fcm_async(register_ids, data):
    p = Process(target=fcm, args=(register_ids, data))
    p.start()


# TODO: send notification to pusher
# TODO: send notification to GCM

# TODO: pusher function wrapper with multiprocess
# TODO: GCM function wrapper with multiprocess
