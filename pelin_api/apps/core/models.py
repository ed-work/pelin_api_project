import urllib2
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)


def upload_to(self, filename):
    """
    generate destination ImageField to the following pattern:
    MEDIA_ROOT/<user nim>_<username>/profile.jpg
    """
    name = "profile." + filename.split(".")[1]
    return "%s_%s/%s" % (self.user.nim, self.user.username, name)


STATUS_CHOICES = (
    (1, 'Teacher'),
    (2, 'Student')
)

MAJOR_CHOICES = (
    (1, 'S1 TI'),
    (2, 'D3 TI'),
    (3, 'D3 MI')
)


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def generate_filename(self, filename):
    """
    generate destination FileField filename arg to the following pattern:
    MEDIA_ROOT/<group_name>_<group_id>/filename
    """
    filename = urllib2.unquote(filename)
    return "groups/%s/%s" % (self.pk, filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('User must have a valid email')
        if not password:
            raise ValueError('User must have a valid password')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)

    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    # photo_thumb

    status = models.IntegerField(
        choices=STATUS_CHOICES, default=2)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def is_teacher(self):
        return self.status == 1

    def get_profile(self):
        if self.is_teacher():
            return self.teacher
        return self.student


class Teacher(models.Model):
    user = models.OneToOneField(User)
    nik = models.CharField(max_length=15, blank=True)
    username = models.CharField(
        _('username'), max_length=30, unique=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                  'This value may contain only letters, numbers '
                  'and @/./+/-/_ characters.'),
                'invalid'),
        ],
        error_messages={
            'unique': _(
                "A user with that username already exists."),
        })

    def __unicode__(self):
        return self.user.first_name


class Student(models.Model):
    user = models.OneToOneField(User)
    nim = models.CharField(
        max_length=12, unique=True,
        error_messages={
            'unique': _(
                "A student with that nim already exists."),
        })

    major = models.IntegerField(choices=MAJOR_CHOICES, default=1)

    def __unicode__(self):
        return self.user.first_name
