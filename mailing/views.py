from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.models import Mailing
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm
from message.models import Message
from client.models import Client
from log.models import Log
from message.forms import MessageFrom
from client.forms import ClientForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from mailing.utils import check_status_mailing, mailing_execution
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        if self.object.name is None:
            self.object.name = f'Mailing №{self.object.pk}'
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
            self.object.status = check_status_mailing(self.object)

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


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'main/mailing_info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = Message.objects.filter(mailing=self.object).last()
        context["clients"] = Client.objects.filter(mailing=self.object).all()
        context["logs"] = Log.objects.filter(mailing=self.object).all()
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing_list')

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
            self.object.status = check_status_mailing(self.object)
        else:
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing_formset = inlineformset_factory(Mailing, Message, form=MessageFrom, extra=0)
        client_formset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['mailing_formset'] = mailing_formset(self.request.POST, instance=self.object)
            context_data['client_formset'] = client_formset(self.request.POST, instance=self.object)
        else:
            context_data['mailing_formset'] = mailing_formset(instance=self.object)
            context_data['client_formset'] = client_formset(instance=self.object)

        return context_data


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_list = sorted(Mailing.objects.filter(user=self.request.user).all(), key=lambda object: object.pk, reverse=True)
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
        context["mailing_list"] = result_list
        context["finished_list"] = finished_list
        if len(finished_list) > 0:
            context["number_finished_mailings"] = len(finished_list)
        else:
            context["number_finished_mailings"] = False
        return context


def mailing_go(request, pk):
    mailing_execution(pk)
    return redirect(request.META.get('HTTP_REFERER'))


def mailing_finish(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.status = 'Finished'
    mailing.save()
    return redirect(request.META.get('HTTP_REFERER'))


def mailing_change_status(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if mailing.status == 'Canceled':
        mailing.status = check_status_mailing(mailing)
    else:
        mailing.status = 'Canceled'
    mailing.save()
    return redirect(request.META.get('HTTP_REFERER'))


def mailing_again(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.status = check_status_mailing(mailing)
    mailing.save()
    return redirect(request.META.get('HTTP_REFERER'))
