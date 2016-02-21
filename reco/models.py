from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    blog = models.URLField(blank=True)
    name = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.user.username



class Comment(models.Model):
    author = models.ForeignKey(UserProfile, null=True, blank=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length = 128, blank = True, null = True)

    def __str__(self):
        return self.content 

    def save(self, *args, **kwargs):
        if self.author:
            self.name = self.author.name
        if not(self.author or self.name):
            self.name = 'unknown'
        super(Comment, self).save(*args, **kwargs)

class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(UserProfile)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    # comments = GenericRelation(Comment, content_type_field = 'content_type',
    #                                     object_id_field = 'object_id')

    def __str__(self):
        return self.title