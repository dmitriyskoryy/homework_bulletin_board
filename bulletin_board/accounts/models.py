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
from django.core.mail import send_mail


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        authors_group = Group.objects.get(name='Authors')
        authors_group.user_set.add(user)
        # user.is_active = 0
        return user




class BasicLoginForm(LoginForm):
    code = CharField(label="Одноразовый код", required=True)
    def __init__(self, *args, **kwargs):
        super(BasicLoginForm, self).__init__(*args, **kwargs)

#
    def user_authenticate(self, *args, **kwargs):
        login = self.request.POST['login']
        password = self.request.POST['password']
        code = self.request.POST['code']
        user = authenticate(self.request, username=login, password=password)
        if user is not None and code == '1':
            print(password, '  ===================== ', login)
            return True
        else:
            print('  ===================== user  None ')
            return False


    def login(self, *args, **kwargs):
        if self.user_authenticate(self, *args, **kwargs):
            return super(BasicLoginForm, self).login(*args, **kwargs)
        else:
            return redirect('/accounts/first_login/')







@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_first_login(request, user, **kwargs):
    try:
        for_user_email = User.objects.get(username=user)

    except:
        raise ObjectDoesNotExist

    code = ''.join(random.choice(string.ascii_letters) for x in range(5))
    message = f"Ваш код для подтверждения аккаунта: {code}"

    html_content = render_to_string(
        'mail_send_code.html',
        {
            'code': message,
            'email': for_user_email.email,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Здравствуйте! Вы зарегистировались на сайте MMORPG. ',
        body=f'Это автоматическая рассылка.',
        from_email=f'dnetdima@gmail.com',
        to=[for_user_email.email, ],
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        # print('send')
        msg.send()
    except:
        raise SMTPDataError(554, 'Сообщение отклонено по подозрению в спаме!')




# @receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_logged_in")
# def user_logged_in(request, user, **kwargs):
#
#     print("======================This not login")