from django.contrib import admin
from .models import User as CustomUser, Teacher, Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'user', 'nim']
    search_fields = ['user__name', 'user__email', 'nim']

    def get_name(self, obj):
        return obj.user.name


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'user', 'nik']
    search_fields = ['user__name', 'user__email', 'nik']

    def get_name(self, obj):
        return obj.user.name


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status']
    search_fields = ['name', 'email']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
