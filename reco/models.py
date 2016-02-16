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
    author = models.ForeignKey(UserProfile, null=True)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content 

class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(UserProfile)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    # comments = GenericRelation(Comment, content_type_field = 'content_type',
    #                                     object_id_field = 'object_id')

    def __str__(self):
        return self.title