from django.contrib import admin
from .models import StudentModel, TeacherModel

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'roll_no','bio', 'skills', 'resume', 'headshot', 'linkedIn_link', 'gitHub_link']
    search_fields = ['name', 'email', 'roll_no']
    list_filter = ['skills']

class TeacherModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
    list_filter = ['name']  # Assuming there are attributes to filter by

admin.site.register(StudentModel, StudentModelAdmin)
admin.site.register(TeacherModel, TeacherModelAdmin)
