from allauth.account.forms import PasswordField
from django.forms import ModelForm, TextInput, CharField
from django.contrib.auth.models import User

class FormOneTimeCode(ModelForm):

    email = CharField(label='Адрес электронной почты:')
    # password = PasswordField(label="Пароль:", autocomplete="current-password")
    code = CharField(label='Одноразовый код:')

    class Meta:
        model = User
        fields = []

    widgets = {
        'email': TextInput(attrs={'size': '80'}),
        'code': TextInput(attrs={'size': '80'}),
    }