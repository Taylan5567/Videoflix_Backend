from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


def build_link(user_instance):
    user_key_bytes = force_bytes(user_instance.pk)
    user_uid = urlsafe_base64_encode(user_key_bytes)
    activation_token = default_token_generator.make_token(user_instance)

    activation_path = reverse(
        'activate',
        kwargs={'uidb64': user_uid, 'token': activation_token}  
    )

    activation_link = f"{settings.SITE_DOMAIN}{activation_path}"

    return activation_link


def send_activation_email(pk):
    user_model = get_user_model()
    user_instance = user_model.objects.get(pk=pk)
    activation_link = build_link(user_instance)

    email_subject_string = render_to_string(
        "activation_subject.txt"
    ).strip()

    email_context_dictionary = {
        "user_email_string": user_instance.email,
        "activation_link_string": activation_link,
    }

    email_text_body_string = render_to_string(
        "activation_email.txt",
        email_context_dictionary,
    )
    email_html_body_string = render_to_string(
        "activation_email.html",
        email_context_dictionary,
    )

    email_message_instance = EmailMultiAlternatives(
        subject=email_subject_string,
        body=email_text_body_string,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_instance.email],
    )

    email_message_instance.attach_alternative(email_html_body_string, "text/html")
    email_message_instance.send(fail_silently=False)