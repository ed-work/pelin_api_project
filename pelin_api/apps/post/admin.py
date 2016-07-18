from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_text', 'group', 'created_at']
    search_fields = ['user__name', 'user__student__nim', 'group__title']

    def get_name(self, obj):
        return obj.user.name

    def get_text(self, obj):
        return obj.text[:20] + '...'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
