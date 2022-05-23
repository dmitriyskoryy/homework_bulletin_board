
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from loguru import logger

from bulletin_board.utils import get_onetime_code, send_message_on_email

@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_first_login(request, user, **kwargs):
    """Функция-сигнал для отслеживания регистрации нового пользователя,
    и отправки ему одноразового кода для подтверждения регистрации"""
    try:
        user = User.objects.get(username=user)
    except ObjectDoesNotExist as e:
        logger.error(e)
        return None

    code = get_onetime_code(user)
    email = user.email
    message = f"Ваш код для подтверждения аккаунта:"
    subject = f'Здравствуйте, {user}! Вы зарегистировались на сайте MMORPG.'
    template = 'mail_send_code.html'
    # send_message_on_email(message, subject, template, email, code)
    send_message_on_email(message, subject, template, email, code=code)
