from django.contrib import admin
from .models import Assignment, SubmittedAssignment


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'due_date']
    search_fields = ['title', 'group__title']
    ordering = ['-due_date']


class SubmittedAssignmentAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'assignment', 'created_at']
    search_fields = ['user__name', 'user__student__nim', 'assignment__title']

    def get_user_name(self, obj):
        return "%s (%s)" % (obj.user.name, obj.user.student.nim)

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(SubmittedAssignment, SubmittedAssignmentAdmin)
