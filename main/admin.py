from django.contrib import admin

# Register your models here.
from client.models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_manager')
