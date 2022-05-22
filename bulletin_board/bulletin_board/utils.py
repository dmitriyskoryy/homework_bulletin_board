import string
from random import choice

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPDataError
from django.core.exceptions import ObjectDoesNotExist

from loguru import logger

from ads.models import OneTimeCode


def send_message_on_email(message, subject, template, email=None, adt=None):
    """Функция отправки сообщения на почту"""

    # message = kwargs['message']
    # subject = kwargs['subject']
    # template = kwargs['template']
    # email = kwargs['email']
    # adt = kwargs['adt']
    # adt = 'sdf'

    html_content = render_to_string(
        f'{template}',
        {
            'adt': adt,
            'message': message,
            'email': email,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{subject}',
        body=f'Это автоматическая рассылка.',
        from_email=f'dnetdima@gmail.com',
        to=[email, ],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        #print("send message ok")
        msg.send()
    except:
        logger.add('logs.log', level='ERROR')
        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')




def onetime_code_create(user):
    """Метод для создания одноразового кода и добавления его в модель OneTimeCode"""
    code = ''.join(choice(string.ascii_letters) for x in range(5))
    OneTimeCode.objects.create(oneTimeCode=code, codeUser=user)



def get_onetime_code(user):
    """Функция для получения одноразового кода пользователя из модели OneTimeCode"""
    try:
        codeUser = OneTimeCode.objects.get(codeUser__username=user)
    except ObjectDoesNotExist as e:
        print(e)
        return None

    if codeUser:
        return codeUser.oneTimeCode
    else:
        return None