from django.contrib import admin
from users.models import User
from mailing.models import Periodicity, Mailing
from article.models import Article
from message.models import Message
from client.models import Client
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_manager')


@admin.register(Periodicity)
class PeriodicityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'vars')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data_mailing',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'mailing')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'mailing')


@admin.register(Article)
class UserAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'text', 'blog_image', 'is_published')
