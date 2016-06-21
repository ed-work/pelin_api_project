from django.contrib import admin
from .models import Group, PendingApproval


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_teacher', 'teacher']
    search_fields = ['title', 'teacher__name']
    ordering = ['title']

    def get_teacher(self, obj):
        return obj.teacher.name


def approve_all(modeladmin, request, queryset):
    for pending in queryset:
        if pending.user not in pending.group.members.all():
            pending.group.members.add(pending.user)
    queryset.delete()
approve_all.short_description = 'Approve selected'


class PendingApprovalAdmin(admin.ModelAdmin):
    list_display = ['group', 'name', 'nim', 'created_at']
    search_fields = ['user__name', 'user__student__nim', 'group__title']
    ordering = ['group__title']
    actions = [approve_all]

    def name(self, obj):
        return obj.user.name

    def nim(self, obj):
        return obj.user.student.nim

    def group(self, obj):
        return obj.group.title


admin.site.register(Group, GroupAdmin)
admin.site.register(PendingApproval, PendingApprovalAdmin)
