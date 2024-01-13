from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from users.forms import UserRegisterForm, UserForm, AuthenticationForm
from users.utils import send_email_for_verify
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing
from message.models import Message
from client.models import Client
from log.models import Log
import random

# Create your views here.


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('index')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_email_for_verify(self.request, new_user)
        #send_mail(
        #    subject='Congratulations',
        #    message='You registered',
        #    from_email=EMAIL_HOST_USER,
        #    recipient_list=[new_user.email]
        #)
        return redirect(reverse('login'))


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('user_update')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    mailing_list = sorted(Mailing.objects.filter(user=user).all(), key=lambda object: object.pk,
                          reverse=True)
    finished_list = []
    result_list = []
    if len(mailing_list) > 0:
        for mailing in mailing_list:
            result = {
                "mailing": mailing,
                "message": Message.objects.filter(mailing=mailing).last(),
                "number_of_clients": len(Client.objects.filter(mailing=mailing).all()),
                "number_of_times": len(Log.objects.filter(mailing=mailing).all()),
                "last_time": Log.objects.filter(mailing=mailing).last(),
            }
            if mailing.status == 'Ready':
                result['ready'] = True
            if mailing.status in ['Finished', 'Canceled']:
                finished_list.append(result)
            else:
                result_list.append(result)
    context = {
        "object": user,
        "mailing_list": result_list,
        "finished_list": finished_list
    }
    if len(finished_list) > 0:
        context["number_finished_mailings"] = len(finished_list)
    else:
        context["number_finished_mailings"] = False
    return render(request, 'users/user_info.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('user_email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            send_mail(
                subject='New password',
                message=f'Your new password {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            user.set_password(new_password)
            user.save()
            return redirect(reverse('login'))
        except Exception:
            message = 'We can not find user with this email'
            context = {
                'message': message
            }
            return render(request, 'users/forgot_password.html', context)
    else:
        return render(request, 'users/forgot_password.html')


def moderator_mailings(request):
    mailing_list = sorted(Mailing.objects.all(), key=lambda object: object.pk, reverse=True)
    finished_list = []
    result_list = []
    if len(mailing_list) > 0:
        for mailing in mailing_list:
            result = {
                "mailing": mailing,
                "message": Message.objects.filter(mailing=mailing).last(),
                "number_of_clients": len(Client.objects.filter(mailing=mailing).all()),
                "number_of_times": len(Log.objects.filter(mailing=mailing).all()),
                "last_time": Log.objects.filter(mailing=mailing).last(),
            }
            if mailing.status in ['Finished', 'Canceled']:
                finished_list.append(result)
            else:
                result_list.append(result)
    context = {
        "mailing_list": result_list,
        "finished_list": finished_list,
    }
    if len(finished_list) > 0:
        context["number_finished_mailings"] = len(finished_list)
    else:
        context["number_finished_mailings"] = False
    return render(request, 'users/moderator_mailings.html', context)


def moderator_users(request):
    users = User.objects.all()
    objects = []
    for user in users:
        number_of_mailings = len(Mailing.objects.filter(user=user).all())
        objects.append({"user": user, "number_of_mailings": number_of_mailings})
    context = {
        "objects": objects
    }
    return render(request, 'users/moderator_users.html', context)


def user_change_active(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(request.META.get('HTTP_REFERER'))
