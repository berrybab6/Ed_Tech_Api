from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from comment.models import Comment

# Create your models here.



def user_directory_path(instance, filename):
    return '{0}/'.format(filename)

class Role(models.Model):

    STUDENT = 1
    TEACHER = 2

    SUPERVISOR = 3
    ADMIN = 4
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()
class UserManager(BaseUserManager):

    def create_user(self, email, username=None, full_name=None, gender=None, profile_url=None, reset_link=None, is_staff=False, password=None, department=None, batch=None, is_active=True, is_student=False, is_admin=False, is_teacher=False):
        if not email:
            raise ValueError("User Must have an email address")
        if not password:
            raise  ValueError("User Must have a Password")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.active = is_active
        user.student = is_student
        user.teacher = is_teacher
        user.gender = gender
        user.department = department
        user.batch = batch
        user.profile_url =profile_url
        user.username = username
        
        user.reset_link = reset_link
        user.full_name = full_name
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None,full_name=None, password=None):

        user = self.create_user(email, username, full_name=full_name, password=password, is_staff=True, is_admin=True)
        return user
    def create_staffuser(self, email, username=None, full_name=None, password=None):
        user = self.create_user(email, username, full_name=full_name, password=password, is_staff=True, is_student=False)
        return user
    def create_teacher(self, email, username, full_name=None, gender=None, department=None, reset_link=None, password=None):
        user = self.create_user(email, username, full_name=full_name, gender=gender, reset_link=reset_link, password=password, department=department, is_teacher=True, is_student=False)
        return user
class User(AbstractUser):
    # roles = models.OneToOneField(Role, on_delete=models.CASCADE, null=True)
    email = models.CharField(unique=True, max_length=255, default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=120, null=True, blank=True)
    profile_url = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    reset_link = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    department = models.CharField(null=True, blank=True, max_length=255)
    batch = models.CharField(null=True, blank=True, max_length=255)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="user", default=None, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_student(self):
        return self.student
    @property
    def is_teacher(self):
        return self.teacher
    @property
    def is_admin(self):
        return self.admin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)