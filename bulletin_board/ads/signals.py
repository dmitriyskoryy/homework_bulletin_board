from smtplib import SMTPDataError

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Respond, Adt, Author

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from bulletin_board.utils import send_message_on_email


# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Respond)
def notify_users_response(sender, instance, **kwargs):
    """Сигнал для отслеживания добавления отклика на объявление. Отправляет письма"""
    respond = Respond.objects.get(pk=instance.id)
    authorAdt = respond.responseAdt
    user = User.objects.get(username=authorAdt.author)
    email = user.email

    message = f"Здравствуйте, {user}! Ваше объявление получило отклик от пользователя {respond.responseUser}"
    subject = f'Ваше объявление на сайте MOPRG получило отклик!'
    template = 'mail_send_response.html'
    send_message_on_email(message, subject, template, email)



@receiver(post_save, sender=Adt)
def notify_new_adt(sender, instance, **kwargs):
    """Сигнал для отслеживания добавления объявления. Отправляет письма"""
    adt = Adt.objects.get(pk=instance.id)

    template = 'mail_send_new_adt.html'

    for user in User.objects.all():
        email = user.email
        message = f"Новое объявление на сайте МMOPRG:"
        subject = f'На сайте МMOPRG новое объявление',
        send_message_on_email(message, subject, template, email, adt)


