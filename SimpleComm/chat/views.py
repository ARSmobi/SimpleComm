from django.shortcuts import render

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm
from .models import User


class UserRegisterView(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'users/register.html'
    success_url = ''

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = '/home/'


def room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
    })
