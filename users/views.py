from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import User
from django.urls import reverse_lazy, reverse

# Create your views here.


class UserCreateView(CreateView):
    model = User
    fields = ["name", "lastname", "birthday", "email"]
    template_name = 'main/user_form.html'

    def get_success_url(self):
        return reverse('user_info', args=[self.object.pk])


class UserDetailView(DetailView):
    model = User
    template_name = 'main/user_info.html'


class UserUpdateView(UpdateView):
    model = User
    template_name = 'main/user_form.html'
    fields = ["name", "lastname", "birthday", "email"]

    def get_success_url(self):
        return reverse('user_info', args=[self.object.pk])


class UserDeleteView(DeleteView):
    model = User
    template_name = 'main/user_confirm_delete.html'
    success_url = reverse_lazy('index')
