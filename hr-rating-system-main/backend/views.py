from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView, CreateView, ListView,FormView,View
from django.views.generic.detail import DetailView
from django.db import IntegrityError
from django.contrib.auth import login, update_session_auth_hash, logout, authenticate
from .models import UsersModel, ListPeopleModel, ListBossModel
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime

__all__ = (
    'signupuserView',
    'LoginView',
    'ListUsersView',
    'ListRatingsView',
    'ChangePasswordView',
    'ChoiseEmp',
    'LogoutPageView',
    'TablePointView',
    'NewEmployedView',
    'TablePointView',
    'error_404_view',
    'NewEmployedView',
    'UpdatePageView',
    'DeletePageView',
    
)
def signupuserView(request):
    if request.method == 'GET':
        return render(request, 'page/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                U = UsersModel(login=request.POST['username'], password=request.POST['password1'])
                U.save()
                login(request, user)
                return redirect('listusersView')
            except IntegrityError:
                return render(request, 'page/signupuser.html', {'form': UserCreationForm(), 'error': 'Такой пользователь уже есть в базе'})
        else:
            return render(request, 'page/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})

class LoginView(View):
    template_name = 'page/loginuser.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            userLogin = UsersModel.objects.get(login=user)
            if userLogin.timeAuthEdit is None:
                userLogin.timeAuthEdit = datetime.now()
                userLogin.save(update_fields=['timeAuthEdit'])
                login(request, user)
                return redirect('change_pass')
            else:
                login(request, user)
                userLogin.timeInput = datetime.now()
                userLogin.save(update_fields=['timeInput'])
                return redirect('listusersView')
        else:
            return render(request, self.template_name, {'form': form})


class LogoutPageView(LogoutView):
    next_page = reverse_lazy('loginuserView')


class ListUsersView(ListView):
    model = ListPeopleModel
    template_name = 'page/listusers.html'
    queryset = ListPeopleModel.objects.exclude(id = 90).exclude(id = 91).order_by('dep', 'name')


class ListRatingsView(DetailView):
    queryset = ListPeopleModel.objects.all()
    success_url = reverse_lazy('main:detail')
    template_name = 'page/modalwindow.html'


class ChoiseEmp(SuccessMessageMixin, UpdateView):
    model = ListPeopleModel
    form_class = UserEvaluationForm
    template_name = 'page/modalwindow.html'
    success_url = reverse_lazy('listusersView')
    success_message = "Оценка успешно добавлена"
    another_message = 'Вы уже проголосовали'
    alert_error = 'Вы не можете голосовать за самого себя'
    boss_error = 'Вы не можете голосовать за своего руководителя'

    def form_valid(self, form):
        id = self.kwargs['pk']
        username = UsersModel.objects.get(login=self.request.user.username)
        if username.isVoted:
            object = ListPeopleModel.objects.get(id=id)
            if username.user_id_id == object.id:
                messages.error(self.request, self.alert_error, extra_tags='bg-danger')
                return redirect(self.success_url)
            else:

                if username.boss_id_id == object.boss_id:
                    messages.error(self.request, self.boss_error, extra_tags='bg-danger')
                    return redirect(self.success_url)
                else:
                    object.responsiveness += int(form.cleaned_data['responsiveness'])
                    object.friendliness += int(form.cleaned_data['friendliness'])
                    object.save(update_fields=['responsiveness'])
                    object.save(update_fields=['friendliness'])
                    username.isVoted = False
                    username.save(update_fields=['isVoted'])
                    messages.success(self.request, self.success_message,extra_tags ='bg-success')
                    return redirect(self.success_url)
        else:
            messages.error(self.request, self.another_message,extra_tags ='bg-danger')
            return redirect(self.success_url)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'page/change_password.html'
    form_class = PasswordChangeForma

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            username = UsersModel.objects.get(login=request.user.username)
            username.password = form.cleaned_data['new_password1']
            username.save(update_fields=['password'])
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('listusersView')
        return render(request, self.template_name, {'form':form})
    
    


class TablePointView(UserPassesTestMixin, ListView):
    model = ListPeopleModel
    template_name = 'page/tablepoint.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
class NewEmployedView(UserPassesTestMixin, ListView):
    model = ListPeopleModel
    template_name = 'page/tablepoint.html'
    success_url = reverse_lazy('main:detail')

    def test_func(self):
        return self.request.user.is_superuser



    
    
@user_passes_test(lambda u: u.is_superuser)    
def NewEmployedView(request):
    success_new = False
    if request.method == 'POST': 
        form = NewEmployedForm(request.POST)
        if form.is_valid():
            form.save()
            success_new = True
    
    template = 'page/newemployed.html'
    context = {
        'list_articles': ListPeopleModel.objects.all().order_by('-id'),
        'form': NewEmployedForm(),
        'update':True,
        'success_new':success_new,
    }
    
    
    return render(request, template,context)

@user_passes_test(lambda u: u.is_superuser)  
def UpdatePageView(request, pk):
    
    success_update = False
    get_article = ListPeopleModel.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = NewEmployedForm(request.POST,instance = get_article)
        if form.is_valid():
            form.save()
            success_update = True
    
    template = 'page/listusers.html'
    
    context = {
        'get_article':get_article,
       'update':True,
       'form': NewEmployedForm(instance = get_article),
       'success_update':success_update,
    }
    return render(request, template, context)

@user_passes_test(lambda u: u.is_superuser)  
def DeletePageView(request,pk):
    get_article = ListPeopleModel.objects.get(pk=pk)
    get_article.delete()
    return redirect(reverse('listusersView'))


def error_403_view(request, exception):
    return render(request, 'page/404.html')
def error_404_view(request, exception):
    return render(request, 'page/404.html')
def error_500_view(request):
    return render(request, 'page/404.html')

# def handler500(request):
#     t = loader.get_template('500_error.html')
#     response = HttpResponseServerError(t.render())
#     response.status_code = 500
#     return response


# class NewEmployedView(UserPassesTestMixin, ListView):
#     model = ListPeopleModel
#     template_name = 'page/newemployed.html'
    
#     def test_func(self):
#         return self.request.user.is_superuser

# class MyModelDeleteView(DeleteView):
#     model = ListPeopleModel
#     success_url = reverse_lazy('listusersView')

