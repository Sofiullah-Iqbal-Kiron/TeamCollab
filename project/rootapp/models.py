from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from .constants import ROLE_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES
from .utils import get_largest_choice


class UserManager(BaseUserManager):
    """ Custom Manager for User Model """

    def create_user(self, username, email, password=None):
        """ Creates and saves a User with given username, email and password. 'username' and 'email' must be unique. """
        
        if not email:
            raise ValueError("Users must have an email address.")
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    # reverse fields: projects
    """ Custom User Model """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150, unique=True, validators=[username_validator], error_messages={"unique": "A user with that username already exists."})
    email = models.EmailField("Email Address", unique=True, error_messages={"unique": "This email already in use."})
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_staff(self):
        """ Close implementation of is_admin. """
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.username


class Project(models.Model):
    # reverse fields: developers, tasks
    name = models.CharField("Project Title", max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='developers')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=len(get_largest_choice(ROLE_CHOICES)), choices=ROLE_CHOICES)

    def __str__(self) -> str:
        return f"{self.project}: {self.user}"


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=len(get_largest_choice(STATUS_CHOICES)), choices=STATUS_CHOICES)
    priority = models.CharField(max_length=len(get_largest_choice(PRIORITY_CHOICES)), choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content
