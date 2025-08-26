from email.mime.image import MIMEImage
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
    """
    Generate an account activation link for the given user instance.

    Args:
        user_instance (User): Instance of the user model.

    Returns:
        str: Full URL string for the user activation link.
    """
    user_key_bytes = force_bytes(user_instance.pk)
    user_uid = urlsafe_base64_encode(user_key_bytes)
    activation_token = default_token_generator.make_token(user_instance)

    activation_link = f"{settings.ACTIVATE_LINK}?uid={user_uid}&token={activation_token}"

    return activation_link


def send_activation_email(pk):
    """
    Send an activation email to the user identified by primary key.

    Args:
        pk (int): Primary key (ID) of the user.
    """
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

    with open("auth_app/templates/img/logo_icon.png", "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo_image>")
        logo.add_header("Content-Disposition", "inline", filename="logo_icon.png")
        email_message_instance.attach(logo)

    email_message_instance.send(fail_silently=False)


def build_link_for_password_reset(user_instance):
    """
    Generate a password reset link for the given user instance.

    Args:
        user_instance (User): Instance of the user model.

    Returns:
        str: Full URL string for the password reset link.
    """
    user_key_bytes = force_bytes(user_instance.pk)
    user_uid = urlsafe_base64_encode(user_key_bytes)
    password_reset_token = default_token_generator.make_token(user_instance)


    password_reset_link = f"{settings.PASSWORD_RESET_LINK}?uid={user_uid}&token={password_reset_token}"

    return password_reset_link


def send_password_reset_email(pk):
    """
    Send a password reset email to the user identified by primary key.

    Args:
        pk (int): Primary key (ID) of the user.
    """
    user_model = get_user_model()
    user_instance = user_model.objects.get(pk=pk)
    password_reset_link = build_link_for_password_reset(user_instance)

    email_subject_string = render_to_string(
        "password_reset_subject.txt"
    ).strip()

    email_context_dictionary = {
        "user_email_string": user_instance.email,
        "password_reset_link_string": password_reset_link,
    }

    email_text_body_string = render_to_string(
        "password_reset_email.txt",
        email_context_dictionary,
    )
    email_html_body_string = render_to_string(
        "password_reset_email.html",
        email_context_dictionary,
    )

    email_message_instance = EmailMultiAlternatives(
        subject=email_subject_string,
        body=email_text_body_string,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_instance.email],
    )

    email_message_instance.attach_alternative(email_html_body_string, "text/html")

    with open("auth_app/templates/img/logo_icon.png", "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo_image>")
        logo.add_header("Content-Disposition", "inline", filename="logo_icon.png")
        email_message_instance.attach(logo)

    email_message_instance.send(fail_silently=False)

