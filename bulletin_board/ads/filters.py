
from django_filters import FilterSet, ModelChoiceFilter
from .models import Respond, Adt, Author
from django.contrib.auth.models import User


# создаём фильтр
class RespondFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.kwargs.get('request')

        # self.fields['responseAdt'].empty_label = "Объявление не выбрано"



    # responseAdt = ModelChoiceFilter(queryset=Respond.objects.filter(responseUser=Author.objects.get(authorUser='admin')), label="Объявление", required=False)

    # responseAdt = ModelChoiceFilter('responseAdt',
    #                         label='Объявление: ',
    #                         lookup_expr='exact',
    #                         queryset=Respond.objects.filter(responseAdt=Adt.objects.all()),
    #                         )

    # в класс мета, надо написать модель, по которой будет строиться форма и нужные нам поля.
    class Meta:
        model = Respond
        fields = ['responseAdt']



    # class Meta:
    #     model = Respond
    #     fields = ['responseAdt__title']



#
# class F(FilterSet):
#     username = CharFilter(method='my_filter')
#
#     class Meta:
#         model = User
#         fields = ['username']
#
#     def my_filter(self, queryset, name, value):
#         return queryset.filter(**{
#             name: value,
#         })
