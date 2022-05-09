
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, CharField, Textarea
from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class FormCreateAdt(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adtCategory'].empty_label = "Категория не выбрана"

    # text = RichTextUploadingField(verbose_name='Текст:')
    text = CharField(widget=CKEditorUploadingWidget(), label='Контент')

    # в класс мета, надо написать модель, по которой будет строиться форма и нужные нам поля.
    class Meta:
        model = Adt
        fields = ['adtCategory', 'title', 'text', ]

        widgets = {
            'title': TextInput(attrs={'size': '100%'}),
            # 'text': Textarea(attrs={'cols': 30, 'rows': 10}),
        }


    #пользовательский валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Длина заголовка не более 255 символов!')

        return title


# removetags:"b span"|