from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_activation_email
from django_rq import get_queue

@receiver(post_save, sender=get_user_model())
def enqueue_activation_email_on_user_create(sender, instance, created, **kwargs):
    """
    Signal receiver that enqueues an activation email task 
    when a new user is created and is not active.

    Parameters:
    sender -- The model class sending the signal (User model)
    instance -- The actual instance being saved
    created -- Boolean; True if new record was created
    kwargs -- Additional keyword arguments

    If the user instance is newly created and inactive, this function
    puts a job onto the default queue to asynchronously send
    an activation email to the user.
    """
    if not created or instance.is_active:
        return

    queue_instance = get_queue("default")
    queue_instance.enqueue(send_activation_email, instance.id, job_timeout=900)


