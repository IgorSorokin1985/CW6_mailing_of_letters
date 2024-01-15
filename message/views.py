from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from message.models import Message
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class MessageCreateView(CreateView):
    model = Message
    fields = ['title', 'body', 'mailing']
    template_name = 'main/message_form.html'

    def get_success_url(self):
        return reverse('message_info', args=[self.object.pk])


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'main/message_info.html'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['title', 'body', 'mailing']
    template_name = 'main/message_form.html'

    def get_success_url(self):
        return reverse('message_info', args=[self.object.pk])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'
    success_url = reverse_lazy('index')
