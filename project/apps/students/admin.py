from re import S
from django.contrib import admin

# Register your models here.

from .models import Student,StudentImportFile,Classroom


admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(StudentImportFile)