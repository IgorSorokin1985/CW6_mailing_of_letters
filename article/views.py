from django.shortcuts import render
from article.models import Article
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

# Create your views here.


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'text', 'blog_image']
    template_name = 'main/article_form.html'

    def get_success_url(self):
        return reverse('article_info', args=[self.object.pk, self.object.slug])


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'main/article_info.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.number_views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)
