from django.contrib import admin

# Register your models here.
from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'is_manager')
