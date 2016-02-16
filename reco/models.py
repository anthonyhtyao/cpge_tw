from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    blog = models.URLField(blank=True)
    name = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(UserProfile)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title 
