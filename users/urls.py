from django.urls import path
from users.views import UserCreateView, UserDetailView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('user_form', UserCreateView.as_view(), name='user_form'),
    path('user_info/<int:pk>/', UserDetailView.as_view(), name='user_info'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
]