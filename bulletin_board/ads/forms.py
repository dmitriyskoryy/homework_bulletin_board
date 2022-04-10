
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *


class FormCreateAdt(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adtCategory'].empty_label = "Категория не выбрана"


    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
    class Meta:
        model = Adt

        fields = ['title', 'text', 'adtCategory',]



    #пользовательский валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Длина заголовка не более 255 символов!')

        return title

