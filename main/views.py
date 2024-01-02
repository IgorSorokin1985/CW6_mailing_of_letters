from django.shortcuts import render
from article.models import Article
import random

# Create your views here.
def index(request):
    articles = Article.objects.all()
    if len(articles) > 0:
        data = {
            'article_1': random.choice(articles),
            'article_2': random.choice(articles),
            'article_3': random.choice(articles),
        }
    else:
        data = {}
    return render(request, 'main/index.html', context=data)
