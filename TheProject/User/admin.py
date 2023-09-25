from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import HomeworkForm

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('date_of_birth', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class HomeworkAdmin(admin.ModelAdmin):
    form = HomeworkForm
    list_display = ('title', 'description', 'date', 'file')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Homework, HomeworkAdmin)