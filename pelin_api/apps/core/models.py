import urllib2

from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)
from versatileimagefield.fields import VersatileImageField


def upload_to(self, filename):
    name = "profile." + filename.split(".")[1]
    return "users/%s/%s" % (self.pk, name)


STATUS_CHOICES = (
    (1, 'Teacher'),
    (2, 'Student')
)

MAJOR_CHOICES = (
    (1, 'S1 TI'),
    (2, 'D3 TI'),
    (3, 'D3 MI'),
    (4, 'S1 DKV')
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

    def get_with(self, key):
        try:
            return self.model.objects.get(student__nim=key)
            # student = Student.objects.select_related('user').get(nim=key)
            # return student.user
        except:
            try:
                # teacher = Teacher.objects.select_related('user').get(username=key)
                # return teacher.user
                return self.model.objects.get(teacher__username=key)
            except:
                return None

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)

    name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    photo = VersatileImageField(upload_to=upload_to, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    status = models.IntegerField(
        choices=STATUS_CHOICES, default=2)

    reg_id = models.CharField(max_length=162, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split(' ')[0]

    def is_teacher(self):
        return self.status == 1

    def get_profile(self):
        return self.teacher if self.is_teacher() else self.student

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)


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
        return self.user.name


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
        return self.user.name


class UserPasswordReset(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=40)
    new_pass = models.CharField(max_length=15)
