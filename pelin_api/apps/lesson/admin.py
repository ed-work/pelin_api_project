from django.contrib import admin
from .models import Lesson, LessonFiles


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'group_name', 'teacher_name']
    search_fields = ['title', 'group__title', 'group__teacher__name']

    def group_name(self, obj):
        return obj.group.title

    def teacher_name(self, obj):
        return obj.group.teacher.name

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonFiles)
