from allauth.account.forms import PasswordField
from django.forms import ModelForm, TextInput, CharField
from django.contrib.auth.models import User

class FormFirstLogin(ModelForm):

    login = CharField(label='Имя пользователя:')
    password = PasswordField(label="Пароль:", autocomplete="current-password")
    code = CharField(label='Одноразовый код:')

    class Meta:
        model = User
        fields = []


    widgets = {
        'login': TextInput(attrs={'size': '80'}),
        'password': TextInput(attrs={'size': '80'}),
        'code': TextInput(attrs={'size': '80'}),
    }