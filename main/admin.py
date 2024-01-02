from django.contrib import admin
from users.models import User
from mailing.models import Periodicity
from article.models import Article
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_manager')


@admin.register(Periodicity)
class PeriodicityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'vars')


@admin.register(Article)
class UserAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'text', 'blog_image', 'is_published')
