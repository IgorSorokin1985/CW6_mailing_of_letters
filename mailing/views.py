from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Mailing
from django.urls import reverse_lazy, reverse

# Create your views here.


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['data_mailing', 'periodicity', 'user']
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_info', args=[self.object.pk])


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing_info.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['data_mailing', 'periodicity', 'user']
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_info', args=[self.object.pk])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('index')
