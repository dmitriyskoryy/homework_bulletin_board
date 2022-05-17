from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import redirect
from django.views import generic

from loguru import logger

from .models import *
from .forms import FormCreateAdt


from django.contrib.auth.models import User

logger.debug("Hello, debug")
logger.info("Hello, info")
logger.error("Hello, error")



class AdtList(generic.ListView):
    model = Adt
    template_name = 'ads_list.html'
    context_object_name = 'ads_list'
    ordering = ['-id']
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_not_group_authors'] = not user.groups.filter(name='Authors').exists()
        return context



class AdtDetailView(generic.DetailView):
    template_name = 'adt_detail.html'
    context_object_name = 'adt'
    queryset = Adt.objects.all() # узнать про это!!!! Надо ли это здесь

    success_url = '/ads/<int:pk>'

    # добавить как-то чтобы после входа автоматов перенаправляло на туже страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        adt = Adt.objects.get(pk=id)
        user = self.request.user

        # получаем все отклики пользователей по объявлению
        response = [r for r in Respond.objects.filter(responseAdt=adt)]
        context['responses_set'] = response

        # проверка может ли пользователь оставлять отклики
        context['is_not_group_common'] = not user.groups.filter(name='Common').exists()

        # проверка является ли пользователь автором текущего объявления
        try:
            context['is_author_adt'] = Adt.objects.filter(pk=id,
                                            author=Author.objects.get(authorUser=user))
        except:
            context['is_author_adt'] = None

        return context





class AdtCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Adt
    template_name = 'adt_create.html'
    form_class = FormCreateAdt
    permission_required = ('ads.add_adt',)

    def form_valid(self, FormCreateAdt):
        self.object = FormCreateAdt.save(commit=False)
        self.object.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(FormCreateAdt)



class AdtUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Adt
    template_name = 'adt_create.html'
    form_class = FormCreateAdt
    permission_required = ('adt.change_adt',)

    # метод get_object  исп вместо queryset, чтобы получить информацию об объекте который нужно редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Adt.objects.get(pk=id)


class AdtDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    template_name = 'adt_delete.html'
    queryset = Adt.objects.all()
    permission_required = ('adt.delete_adt',)
    success_url = '/ads/'




class Personal_Area(LoginRequiredMixin, generic.ListView):
    model = Respond
    template_name = 'personal_area.html'
    context_object_name = 'responses'
    ordering = ['-id']



    def get_queryset(self):
        if self.request.GET.get("q") is not None:
            return Respond.objects.filter(responseAdt__title__icontains=self.request.GET.get("q"))


    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['title'] = [s.title for s in Adt.objects.filter(author=Author.objects.get(authorUser=user))]
        context['q'] = self.request.GET.get("q")
        q = self.request.GET.get("q")

        if self.request.GET.get("id_accept") == "Принять":
            print('====================== ' )
        return context





def user_response(request):
    """Функция добавления отклика на объявление"""
    if request.method == "POST":
        user = request.user
        id_adt = request.POST['id_adt']
        text_response = request.POST['text_response']

        Respond.objects.create(responseUser=User.objects.get(username=user), responseAdt=Adt.objects.get(pk=id_adt), text=text_response)
    return redirect(f'/ads/{id_adt}')






# def usual_login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         print('===================== is not None')
#     else:
#         print('===================== is None')

