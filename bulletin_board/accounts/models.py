from allauth.account.forms import SignupForm, LoginForm

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from django.shortcuts import redirect


from ads.models import Author
from bulletin_board.utils import get_onetime_code, onetime_code_create


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)

        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        authors_group = Group.objects.get(name='Authors')
        authors_group.user_set.add(user)

        Author.objects.create(authorUser=user)
        onetime_code_create(user)
        return user



class BasicLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(BasicLoginForm, self).__init__(*args, **kwargs)

    def user_authenticate(self):
        login = self.request.POST['login']
        password = self.request.POST['password']

        user = authenticate(self.request, username=login, password=password)
        if user is not None:
            user_code = get_onetime_code(user)
        else:
            return False

        if user_code is None:
            return True


    def login(self, *args, **kwargs):
        if self.user_authenticate():
            return super(BasicLoginForm, self).login(*args, **kwargs)
        else:
            return redirect(f"/accounts/first_login/")







