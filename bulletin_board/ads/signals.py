from smtplib import SMTPDataError

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Respond, Adt, Author
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Respond)
def notify_users_response(sender, instance, **kwargs):

    respond = Respond.objects.get(pk=instance.id)
    # categoryes = [s.name for s in adt.postCategory.all()]

    authorAdt = respond.responseAdt
    user = User.objects.get(username=authorAdt.author)
    email_author_adt = user.email



    message = f"Здравствуйте, {user}! Ваше объявление получило отклик от пользователя {respond.responseUser}"

    html_content = render_to_string(
        'mail_send_response.html',
        {
            'message': message,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Ваше объявление на сайте MOPRG получило отклик!',
        body=f'Это автоматическая рассылка.',
        from_email=f'dnetdima@gmail.com',
        to=[email_author_adt, ],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        #print("user     ", user.email)
        msg.send()
    except:
        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')

