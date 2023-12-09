from django.urls import path
from message.views import MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView

urlpatterns = [
    path('message_form/', MessageCreateView.as_view(), name='message_form'),
    path('message_info/<int:pk>', MessageDetailView.as_view(), name='message_info'),
    path('message_form/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]