import logging

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
import uuid as uuid_lib

from .forms import  RegisterForm, ProfileForm, LoginForm

from .models import User
from article.models import Article



logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'user/index.html'
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['more_context'] = Article.objects.all().filter(user_id=self.request.user.uuid)
            number = Article.objects.all().filter(user_id=self.request.user.uuid)
            context['count'] = number.count()
            return context

index = IndexView.as_view()


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': RegisterForm(),
        }
        return render(request, 'user/register.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")

        form = RegisterForm(request.POST)
        # エラーがある際
        if not form.is_valid():
            return render(request, 'user/register.html', {'form': form})

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        auth_login(request, user)

        return redirect('/user/index/')


register = RegisterView.as_view()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "ログインしています。")
            return redirect(reverse('user:index'))

        context = {
            'form': LoginForm(),
        }
        return render(request, 'user/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        forms = LoginForm()
        if not form.is_valid():
            messages.info(request, "正しい値を入力してください。")
            return render(request, 'user/login.html', {'form': forms})

        user = form.get_user()

        auth_login(request, user)

        messages.info(request, "ログインしました。")

        return redirect(reverse('user:index'))


login = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)
            messages.info(request, "ログアウトしました。")
            return redirect('/user/login')
        if not request.user.is_authenticated:
            messages.info(request, "ログインしてください。。")
            return redirect('/user/login')

logout = LogoutView.as_view()


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(request.GET or None, instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'user/profile.html', context)

    def post(self, request, *args, **kwargs):
        logger.info("You're in post!!!")
        form = ProfileForm(request.POST, instance=request.user)
        uuid4 = request.user.uuid
        if not form.is_valid():
            return render(request, 'user/profile.html', {'form': form})

        form.save()

        messages.info(request, "プロフィールを更新しました。")
        return redirect('user:profile', uuid=request.user.uuid)


profile = ProfileView.as_view()
