from django.contrib import admin
from user.models import User
from mailing.models import Periodicity
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_manager')


@admin.register(Periodicity)
class PeriodicityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'vars')
