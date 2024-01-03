from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Mailing
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm
from message.models import Message
from client.models import Client
from message.forms import MessageFrom
from client.forms import ClientForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect

# Create your views here.


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_info', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        context_data = self.get_context_data()
        mailing_formset = context_data['mailing_formset']
        client_formset = context_data['client_formset']
        self.object = form.save()
        self.object.user = self.request.user
        if mailing_formset.is_valid() and client_formset.is_valid():
            mailing_formset.instance = self.object
            mailing_formset.save()
            client_formset.instance = self.object
            client_formset.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing_formset = inlineformset_factory(Mailing, Message, form=MessageFrom, extra=1)
        client_formset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['mailing_formset'] = mailing_formset(self.request.POST)
            context_data['client_formset'] = client_formset(self.request.POST)
        else:
            context_data['mailing_formset'] = mailing_formset()
            context_data['client_formset'] = client_formset()

        return context_data


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing_info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = Message.objects.filter(mailing=self.object).all()
        print(context["message"])
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_info', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        context_data = self.get_context_data()
        mailing_formset = context_data['mailing_formset']
        client_formset = context_data['client_formset']
        self.object = form.save()
        self.object.user = self.request.user
        if mailing_formset.is_valid() and client_formset.is_valid():
            mailing_formset.instance = self.object
            mailing_formset.save()
            client_formset.instance = self.object
            client_formset.save()
        else:
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing_formset = inlineformset_factory(Mailing, Message, form=MessageFrom, extra=0)
        client_formset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=0)
        if self.request.method == 'POST':
            context_data['mailing_formset'] = mailing_formset(self.request.POST, instance=self.object)
            context_data['client_formset'] = client_formset(self.request.POST, instance=self.object)
        else:
            context_data['mailing_formset'] = mailing_formset(instance=self.object)
            context_data['client_formset'] = client_formset(instance=self.object)

        return context_data


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('index')

class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_list = sorted(Mailing.objects.filter(user=self.request.user).all(), key=lambda object: object.pk, reverse=True)
        #Mailing.objects.filter(user=self.request.user).all()
        result_list = []
        for mailing in mailing_list:
            result = {
                "mailing": mailing,
                "message": Message.objects.filter(mailing=mailing).last(),
                "clients": Client.objects.filter(mailing=mailing).all(),
            }
            result_list.append(result)
        context["mailing_list"] = result_list
        return context
