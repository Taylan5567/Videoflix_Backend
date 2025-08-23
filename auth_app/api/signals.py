from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_activation_email
from django_rq import get_queue

@receiver(post_save, sender=get_user_model())
def enqueue_activation_email_on_user_create(sender, instance, created, **kwargs):
    if not created or instance.is_active:
        return

    queue_instance = get_queue("default")
    queue_instance.enqueue(send_activation_email, instance.id, job_timeout=900)


