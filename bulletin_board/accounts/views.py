from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import generic
from .forms import FormFirstLogin
from .models import BasicSignupForm

import allauth.account.views
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class FirstLoginView(generic.CreateView):
    template_name = 'accounts/first_login.html'
    form_class = FormFirstLogin
    # success_url = '/accounts/login'




def register_code(request):
    if request.method == "POST":
        print('=========================   Принять', request.POST['login'])
        print('=========================   Принять', request.POST['password'])
        print('=========================   Принять', request.POST['code'])

    return redirect(f'/ads/')


# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BasicSignupForm
#     success_url = '/ads/'

#
#
# @receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_logged_in")
# def user_logged_in(request, user, **kwargs):
#     try:
#         for_user_email = User.objects.get(username=user)
#         for_user_email.is_activate = 0
#         print("user_logged_in ======================")
#     except:
#             raise ObjectDoesNotExist
