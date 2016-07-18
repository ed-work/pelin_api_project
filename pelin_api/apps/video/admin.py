from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_id',
                    'get_name', 'user', 'get_categories']
    search_fields = ['title', 'user__name', 'description', 'category__name']

    def get_name(self, obj):
        return obj.user.name

    def get_categories(self, obj):
        tags = []
        for tag in obj.category.all():
            tags.append(str(tag))
        return ', '.join(tags)

admin.site.register(Video, VideoAdmin)
