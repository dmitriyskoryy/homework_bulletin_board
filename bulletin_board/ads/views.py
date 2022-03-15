from django.views import generic
from .models import Adt


class AdtList(generic.ListView):
    model = Adt
    template_name = 'ads_list.html'
    context_object_name = 'ads_list'
    ordering = ['-id']
    paginate_by = 10


