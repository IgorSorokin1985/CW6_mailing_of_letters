from django.urls import path
from mailing.views import MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView

urlpatterns = [
    path('mailing_form/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailing_info/<int:pk>', MailingDetailView.as_view(), name='mailing_info'),
    path('mailing_form/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailind_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
]
