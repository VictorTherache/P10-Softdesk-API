"""
"""
from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User Model
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Projet(models.Model):
    """
    Project Model
    """
    title= models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    type = CharField(max_length=200)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.title


class Issue(models.Model):
    """
    Issue Model
    """
    title= models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    tag = models.CharField(max_length=300)
    priority = models.CharField(max_length=300)
    status = models.CharField(max_length=300)
    projet = models.ForeignKey(Projet, related_name='issues', on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_user'
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Contributor(models.Model):
    """
    Contributor model
    """
    CHOICES = (
        ('A', 'Author'),
        ('C', 'Contributor'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, related_name='contributors', on_delete=models.CASCADE)
    permission = models.CharField(max_length=200, choices=CHOICES)
    role = models.CharField(max_length=200)
    def __str__(self):
        return str(self.user)


class Comments(models.Model):
    """
    Comment model
    """
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    issue = models.ForeignKey(Issue, related_name='comments', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.description
