import requests
import json
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
    for reg_id in register_ids:
        data = {
            'data': {
                'teacher_name': data['actor']['name'],
                'verb': data['verb'],
                'group_title': data['target']['title'],
                'group_id': data['target']['id'],
                'action_type': data['action_type']
            },
            'to': reg_id
        }
        req = requests.post(settings.FCM_URL,
                            data=json.dumps(data),
                            headers=HEADERS)
        print "%s %s" % (req.status_code, req.reason)


def fcm_async(register_ids, data):
    p = Process(target=fcm, args=(register_ids, data))
    p.start()
