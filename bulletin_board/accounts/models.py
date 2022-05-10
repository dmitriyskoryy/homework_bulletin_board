
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        authors_group = Group.objects.get(name='Authors')
        authors_group.user_set.add(user)
        return user



# class BasicLoginForm(LoginForm):
#     def login(self, request, redirect_url='/'):
#         user = super(BasicLoginForm, self)
#         if user is not None:
#             print("============= is not None")
#         else:
#             print("============= user None")
#         return user


# @receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_logged_in")
# def user_logged_in(request, user, **kwargs):
#
#     print("======================This not login")



@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    try:
        for_user_email = User.objects.get(username=user)
        print(for_user_email.email)
    except:
        raise ObjectDoesNotExist


    # user signed up now send email
    # send email part - do your self