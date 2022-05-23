import string
from random import choice

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPDataError
from django.core.exceptions import ObjectDoesNotExist

from loguru import logger

from ads.models import OneTimeCode

@logger.catch()
# def send_message_on_email(message, subject, template, email=None, adt=None, code=None):
def send_message_on_email(message, subject, template, email, **kwargs):
    """Функция отправки сообщения на почту"""


    adt = kwargs.get('adt')
    code = kwargs.get('code')

    html_content = render_to_string(
        f'{template}',
        {
            'adt': adt,
            'message': message,
            'email': email,
            'code': code,
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
        msg.send()
        #print(message)
    except SMTPDataError as e:
        logger.error(e)




def onetime_code_create(user):
    """Метод для создания одноразового кода и добавления его в модель OneTimeCode"""
    code = ''.join(choice(string.ascii_letters) for x in range(5))
    OneTimeCode.objects.create(oneTimeCode=code, codeUser=user)



def get_onetime_code(user):
    """Функция для получения одноразового кода пользователя из модели OneTimeCode"""
    try:
        codeUser = OneTimeCode.objects.get(codeUser__username=user)
    except ObjectDoesNotExist as e:
        logger.error(e)
        return None

    if codeUser:
        return codeUser.oneTimeCode
    else:
        return None