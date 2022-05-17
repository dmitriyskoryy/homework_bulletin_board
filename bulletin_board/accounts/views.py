from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import generic
from .forms import FormOneTimeCode

from ads.models import OneTimeCode

from .models import BasicSignupForm

import allauth.account.views
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist



class FirstLoginView(generic.CreateView):
    template_name = 'accounts/first_login.html'
    form_class = FormOneTimeCode




def register_code(request):
    """Функция проверки есть ли в модели OneTimeCode пользователь с одноразовым кодом
     и совпадает ли этот код с тем, который был передан в request. Если есть, то данная запись
     удаляется из модели OneTimeCode, тем самым подтверждается регистрация"""
    if request.method == "POST":
        code_request = request.POST['code']
        email = request.POST['email']
        code_user = None
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            # elif User.objects.filter(username=email).exists():
            #     user = User.objects.get(username=email)
                code_user = OneTimeCode.objects.get(codeUser=user)
        except:
            return redirect(f'/accounts/first_login/')


        if code_user is not None:
            if code_user.oneTimeCode == code_request:
                code_user.delete()
                return redirect(f'/accounts/login/')
            else:
                return redirect(f'/accounts/first_login/')



#
# @receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_logged_in")
# def user_logged_in(request, user, **kwargs):
#     try:
#         for_user_email = User.objects.get(username=user)
#         for_user_email.is_activate = 0
#         print("user_logged_in ======================")
#     except:
#             raise ObjectDoesNotExist
