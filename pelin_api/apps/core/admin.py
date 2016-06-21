from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User as CustomUser, Teacher, Student
from .forms import UserCreationForm, UserChangeForm


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


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'status']
    search_fields = ['name', 'email']
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin',
                                    'is_staff', 'is_active',
                                    'user_permissions')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
        ),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin',
                                    'is_staff', 'is_active',
                                    'user_permissions')})
    )

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.exclude(is_superuser=True)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
