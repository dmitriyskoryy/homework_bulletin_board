from django_filters import FilterSet
from .models import Respond


# создаём фильтр
class RespondFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.kwargs.get('request')

    # в класс мета, надо написать модель, по которой будет строиться форма и нужные нам поля.
    class Meta:
        model = Respond
        fields = ['responseAdt']


