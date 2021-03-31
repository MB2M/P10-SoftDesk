from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Project(models.Model):
    type_choices = (
        ('BE','Back-end'),
        ('FE','Front-end'),
        ('IOS','IOS'),
        ('Android', 'Android')
    )
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='Contributor')
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=type_choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_author')

class Contributor(models.Model):
    role_choices = (
        ('contributor','contributor'),
        ('author','author'),
    )
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=100, blank=False)
    role = models.CharField(max_length=100, blank=False, choices=role_choices)

    class Meta:
        unique_together = ['user', 'project']

class Issue(models.Model):
    priority_choices = (
        ('h','high'),
        ('m','middle'),
        ('l', 'low')
    )

    tag_choices = (
        ('b', 'bug'),
        ('i', 'improvement'),
        ('t', 'task')
    )

    status_choices = (
        ('todo', 'to do'),
        ('run', 'running'),
        ('done', 'done')
    )

    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    tag = models.CharField(max_length=300, choices=tag_choices)
    priority = models.CharField(max_length=300, choices=priority_choices)
    project= models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=status_choices)
    author= models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_author')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_assignee')
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue , on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)