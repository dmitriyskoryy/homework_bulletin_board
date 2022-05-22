from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import generic
from .forms import FormOneTimeCode

from ads.models import OneTimeCode


from django.core.exceptions import ObjectDoesNotExist

from loguru import logger

class FirstLoginView(generic.CreateView):
    template_name = 'accounts/first_login.html'
    form_class = FormOneTimeCode



def register_code(request):
    """Функция проверки есть ли в модели OneTimeCode пользователь с одноразовым кодом
     и совпадает ли этот код с тем, который был передан в request. Если есть,
     то данная запись удаляется из модели OneTimeCode, тем самым подтверждается
     регистрация"""
    if request.method == "POST":
        code_request = request.POST['code']
        email = request.POST['email']
        code_user = None
        try:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                code_user = OneTimeCode.objects.get(codeUser=user)
        except ObjectDoesNotExist as e:
            logger.error(e)
            return redirect(f'/accounts/first_login/')


        if code_user is not None:
            if code_user.oneTimeCode == code_request:
                code_user.delete()
                return redirect(f'/accounts/login/')
            else:
                return redirect(f'/accounts/first_login/')



