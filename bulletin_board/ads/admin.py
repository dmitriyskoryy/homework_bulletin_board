from django.contrib import admin
from django.forms import ModelForm, CharField
from .models import *

from ckeditor.widgets import CKEditorWidget

admin.site.register(Category)
admin.site.register(Author)
# admin.site.register(Adt)
admin.site.register(Respond)
admin.site.register(Subscriber)




class AdtAdminForm(ModelForm):
    text = CharField(widget=CKEditorWidget())
    class Meta:
        model = Adt  # Тут нужно указать название можеди в которой мы будем использовать CKEditor
        fields = '__all__'


@admin.register(Adt)
class AdtAdmin(admin.ModelAdmin):
    form = AdtAdminForm