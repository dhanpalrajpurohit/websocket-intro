from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Book
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@receiver(post_save, sender=Book)
def send_new_book_notification(sender, instance, created, **kwargs):
    # if created:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'book_notifications',  # Group name
        {
            'type': 'send_notification',
            'message': f'A new book "{instance.title}" has been added!'
        }
    )
