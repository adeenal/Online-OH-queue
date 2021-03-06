from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.conf import settings


from .forms import StudentUserCreationForm, StudentUserChangeForm
from .models import StudentUser
import os

class StudentUserAdmin(UserAdmin):
    add_form = StudentUserCreationForm
    form = StudentUserChangeForm
    model = StudentUser
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_active', 'is_ta', 'is_superuser']
    fieldsets = (
        ('User Information', {'fields': ('first_name', 'last_name', 'email', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_ta', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined',)})
    )
    list_filter = ('is_superuser', 'is_ta', 'is_active')

admin.site.site_header = os.environ.get('COURSE_TITLE','')  + ' Office Hours Admin'
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.unregister(Group)