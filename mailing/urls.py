from django.urls import path
from mailing.views import MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, MailingListView

urlpatterns = [
    path('mailing_form/', MailingCreateView.as_view(), name='mailing_form'),
    path('mailing_info/<int:pk>', MailingDetailView.as_view(), name='mailing_info'),
    path('mailing_form/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
]
