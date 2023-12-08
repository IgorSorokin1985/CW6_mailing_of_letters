from django.urls import path
from main.views import index
from article.views import ArticleCreateView


urlpatterns = [
    path('', index),
]
