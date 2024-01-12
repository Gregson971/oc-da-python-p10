from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time')


admin.site.register(User, UserAdmin)
