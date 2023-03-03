from django.contrib import admin

from .models import EmployeeData, UserData

# Register your models here.
admin.site.register(EmployeeData)
admin.site.register(UserData)
