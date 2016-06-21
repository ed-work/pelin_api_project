from django.contrib import admin
from .models import Group, PendingApproval


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_teacher', 'teacher']
    search_fields = ['title', 'teacher__name']

    def get_teacher(self, obj):
        return obj.teacher.name

admin.site.register(Group, GroupAdmin)
# TODO: custom action
admin.site.register(PendingApproval)
