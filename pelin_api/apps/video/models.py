from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from apps.core.models import User, TimeStamped
from django_extensions.db.models import TitleDescriptionModel


class Video(TimeStamped, TitleDescriptionModel):
    user = models.ForeignKey(User, related_name='uploaded_videos')
    slug = models.SlugField(null=True, blank=True)
    category = TaggableManager(blank=True)
    youtube_id = models.CharField(max_length=11)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)
