from django.db import models
from django.template.defaultfilters import slugify
# from taggit.managers import TaggableManager
from apps.core.models import User

CATEGORY_CHOICES = (
    ('Umum', 'Umum'),
    ('RPL', 'RPL'),
    ('Multimedia', 'Multimedia'),
    ('Jaringan', 'Jaringan')
)


class Video(models.Model):
    user = models.ForeignKey(User, related_name='uploaded_videos')
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    file = models.FileField()
    # category = TaggableManager()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)
