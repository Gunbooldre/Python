from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView, CreateView, ListView,FormView,View
from django.views.generic.detail import DetailView
from django.db import IntegrityError
from django.contrib.auth import login, update_session_auth_hash, logout, authenticate
from .models import UsersModel, ListPeopleModel
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from datetime import datetime

__all__ = (
    'signupuserView',
    'loginuserView',
    #'logoutuserView',
    'LoginView',
    'ListUsersView',
    'ListRatingsView',
    'ChangePasswordView',
    'ChoiseEmp',
    'LogoutPageView',
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
        form = LoginForm()
        return render(request, 'page/loginuser.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Do something with the valid data, e.g. log the user in
            return redirect('listusersView')
        return render(request, 'page/loginuser.html', {'form': form})

def loginuserView(request):
    if request.method == 'GET':
        return render(request, 'page/loginuser.html', {'form': AuthenticationForm()})
    else:

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        user_name = authenticate(request, username=request.POST['username'])
        passs = authenticate(request, password=request.POST['password'])
        if user:

            username = UsersModel.objects.get(login=user)
            if username.timeAuthEdit is None:
                username.timeAuthEdit = datetime.now()
                username.save(update_fields=['timeAuthEdit'])
                login(request, user)
                return redirect('change_pass')
            else:
                login(request, user)
                username.timeInput = datetime.now()
                username.save(update_fields=['timeInput'])
                return redirect('listusersView')
        else:
            return render(request, 'page/loginuser.html', {'form': AuthenticationForm(), 'error': 'Пользователь или пароль не соотвествует'})


# def logoutuserView(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('loginuserView')
#
class LogoutPageView(LogoutView):
    next_page = reverse_lazy('loginuserView')


class ListUsersView(ListView):
    model = ListPeopleModel
    template_name = 'page/listusers.html'


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

    def form_valid(self, form):
        id = self.kwargs['pk']
        username = UsersModel.objects.get(login=self.request.user.username)
        if username.isVoted:
            object = ListPeopleModel.objects.get(id=id)
            object.responsiveness += int(form.cleaned_data['responsiveness'])
            object.friendliness += int(form.cleaned_data['friendliness'])
            object.save(update_fields=['responsiveness'])
            object.save(update_fields=['friendliness'])
            username.isVoted = False
            username.save(update_fields=['isVoted'])
            messages.success(self.request, self.success_message,extra_tags ='alert-success')
            return redirect(self.success_url)
        else:
            messages.error(self.request, self.another_message,extra_tags ='alert-danger')
            return redirect(self.success_url)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'page/change_password.html'
    form_class = PasswordChangeForm

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