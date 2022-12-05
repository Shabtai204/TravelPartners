from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

import string
import random


def rand_slug():
    return ''.join(random.choice(string.digits) for _ in range(6))


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    slug = models.SlugField(null=False, unique=True)

    USERNAME_FIELDS = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Trip(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    start_loc = models.CharField(max_length=50)
    end_loc = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + rand_slug())
        return super().save(*args, **kwargs)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.body + "-" + rand_slug())
        return super().save(*args, **kwargs)
