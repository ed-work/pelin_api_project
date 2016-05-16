# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .serializers import NotificationSerializer
# from notifications.models import Notification
# from .realtime import pusher_async


# @receiver(post_save, sender=Notification)
# def notif_post_save(sender, instance, **kwargs):
#     pusher_async(str(instance.recipient_id), 'new-notif', instance)
