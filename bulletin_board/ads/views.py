from django.shortcuts import redirect
from django.views import generic
from .models import *
from .forms import FormCreateAdt

class AdtList(generic.ListView):
    model = Adt
    template_name = 'ads_list.html'
    context_object_name = 'ads_list'
    ordering = ['-id']
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user
        # context['is_not_authors'] = not user.groups.filter(name='authors').exists()
        context['is_not_authors'] = ''

        return context


class AdtDetailView(generic.DetailView):
    template_name = 'adt_detail.html'
    context_object_name = 'adt'
    queryset = Adt.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        id = self.kwargs.get('pk')
        adt = Adt.objects.get(pk=id)


        # получаем все отклики пользователей по объявлению

        response = [r for r in Respond.objects.filter(responseAdt=adt)]
        context['responses_set'] = response
        return context





class AdtCreateView(generic.CreateView):
    model = Adt
    template_name = 'adt_create.html'
    form_class = FormCreateAdt

    def form_valid(self, FormCreateAdt):
        self.object = FormCreateAdt.save(commit=False)
        self.object.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(FormCreateAdt)



class AdtUpdateView(generic.UpdateView):
    model = Adt
    template_name = 'adt_create.html'
    form_class = FormCreateAdt

    # метод get_object  исп вместо queryset, чтобы получить информацию об объекте который нужно редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Adt.objects.get(pk=id)


class AdtDeleteView(generic.DeleteView):
    template_name = 'adt_delete.html'
    queryset = Adt.objects.all()
    success_url = '/ads/'






def user_response(request):
    if request.method == "POST":
        user = request.user
        id_adt = request.POST['id_adt']
        text_response = request.POST['text_response']

        Respond.objects.create(responseUser=User.objects.get(username=user), responseAdt=Adt.objects.get(pk=id_adt), text=text_response)

    return redirect(f'/ads/{id_adt}')




