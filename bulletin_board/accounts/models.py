import random
import string
from smtplib import SMTPDataError

from allauth.account.forms import SignupForm, LoginForm

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.forms import CharField
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


from django.contrib.auth.models import User


from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from ads.models import OneTimeCode, Author


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)

        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        authors_group = Group.objects.get(name='Authors')
        authors_group.user_set.add(user)

        Author.objects.create(authorUser=user)
        self.code_create(user)
        return user



    def code_create(self, user):
        """Метод для создания одноразового кода и добавления его в модель OneTimeCode"""
        code = ''.join(random.choice(string.ascii_letters) for x in range(5))
        OneTimeCode.objects.create(oneTimeCode=code, codeUser=user)



class BasicLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(BasicLoginForm, self).__init__(*args, **kwargs)

    def user_authenticate(self):
        login = self.request.POST['login']
        password = self.request.POST['password']

        user = authenticate(self.request, username=login, password=password)
        if user is not None:
            user_code = get_one_time_code(user)
        else:
            return False

        if user_code is None:
            return True


    def login(self, *args, **kwargs):
        if self.user_authenticate():
            return super(BasicLoginForm, self).login(*args, **kwargs)
        else:
            return redirect(f"/accounts/first_login/")



def get_one_time_code(user):
    """Функция для получения одноразового кода пользователя из модели OneTimeCode"""
    try:
        codeUser = OneTimeCode.objects.get(codeUser__username=user)
    except:
        return None

    if codeUser:
        return codeUser.oneTimeCode
    else:
        return None



@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_first_login(request, user, **kwargs):
    """Функция-сигнал для отслеживания регистрации нового пользователя,
    и отправки ему одноразового кода для подтверждения регистрации"""
    try:
        user = User.objects.get(username=user)
    except:
        raise ObjectDoesNotExist

    user_code = get_one_time_code(user)

    message = f"Ваш код для подтверждения аккаунта: {user_code}"

    html_content = render_to_string(
        'mail_send_code.html',
        {
            'code': message,
            'email': user.email,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Здравствуйте, {user}! Вы зарегистировались на сайте MMORPG. ',
        body=f'Это автоматическая рассылка.',
        from_email=f'dnetdima@gmail.com',
        to=[user.email, ],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        print(user_code, "   ", user)
        # msg.send()
    except:
        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')




# @receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_logged_in")
# def user_logged_in(request, user, **kwargs):
#
#     print("======================This not login")