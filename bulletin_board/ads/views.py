from django.shortcuts import redirect
from django.views import generic
from .models import *
from .forms import FormCreateAdt
from .filters import RespondFilter

from django.contrib.auth.models import User

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





class Personal_Area(generic.ListView):
    model = Respond
    template_name = 'personal_area.html'
    context_object_name = 'responses'
    ordering = ['-id']
    success_url = '/ads/personal_area'


    def get_queryset(self):
        if self.request.GET.get("q") is not None:
            return Respond.objects.filter(responseAdt__title__icontains=self.request.GET.get("q"))


    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['title'] = [s.title for s in Adt.objects.filter(author=Author.objects.get(authorUser=user))]
        context['q'] = self.request.GET.get("q")
        return context



    # def get_filter(self):
    #     return RespondFilter(self.request.GET, queryset=super().get_queryset())
    #
    # def get_queryset(self):
    #     return self.get_filter().qs
    #
    # def get_context_data(self, *args, **kwargs):
    #     user = self.request.user
    #     context = super().get_context_data(**kwargs)
    #     # captions_adt = [s.responseAdt.title for s in Respond.objects.filter(responseUser=user)]
    #     return {
    #         **super().get_context_data(*args, **kwargs),
    #         "filter": self.get_filter(),
    #
    #         # "title": captions_adt,
    #     }






# def user_list(request):
#     f = F(request.GET, queryset=User.objects.all())
#     return render(request, 'user_t.html', {'filter': f})







def user_response(request):
    if request.method == "POST":
        user = request.user
        id_adt = request.POST['id_adt']
        text_response = request.POST['text_response']

        Respond.objects.create(responseUser=User.objects.get(username=user), responseAdt=Adt.objects.get(pk=id_adt), text=text_response)

    return redirect(f'/ads/{id_adt}')



def accept_response(request):
    if request.method == "POST":

        print('=========================   Принять', request.POST['id_accept'])

        print('=========================   Удалить', request.POST['id_delete'])

    return redirect(f'/ads/personal_area/')
