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
    """Сигнал для отслеживания добавления отклика на объявление и отправки письма"""
    respond = Respond.objects.get(pk=instance.id)
    authorAdt = respond.responseAdt
    user = User.objects.get(username=authorAdt.author)
    email = user.email


    message = f"Здравствуйте, {user}! Ваше объявление получило отклик от пользователя {respond.responseUser}"

    subject = f'Ваше объявление на сайте MOPRG получило отклик!'

    send_message_on_email(message, subject, email)




@receiver(post_save, sender=Adt)
def notify_new_adt(sender, instance, **kwargs):
    """Сигнал для отслеживания добавления объявления и отправки письма"""

    adt = Adt.objects.get(pk=instance.id)


    for user in User.objects.all():
        message = f"Спешите прочитать новое объявление сайте МMOPRG:"

        html_content = render_to_string(
            'mail_send_new_adt.html',
            {
                'adt': adt,
                'message': message,
                'email': user.email,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'На сайте МMOPRG новое объявление',
            body=f'Это автоматическая рассылка.',
            from_email=f'dnetdima@gmail.com',
            to=[user.email, ],
        )
        msg.attach_alternative(html_content, "text/html")

        try:
            #print("user     ", user.email)
            msg.send()
        except:
            raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')

