from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models
from reco.functions import latexToHtml
import subprocess
from django.conf import settings

class User(AbstractUser):
    blog = models.URLField(blank=True)
    ispublic = models.BooleanField(default=True)
    highschool = models.CharField(max_length = 128, blank=True, null = True)
    prepa = models.CharField(max_length = 128, blank=True, null = True)
    grandsecole = models.CharField(max_length = 128, blank=True,  null = True)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
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
    slg = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True)
    contentLtx = models.TextField(null=True)
    contentHtml = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    abstract = models.CharField(max_length=256,null=True)
    # comments = GenericRelation(Comment, content_type_field = 'content_type',
    #                                     object_id_field = 'object_id')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slg = slugify(self.title)
        latexToHtml(self.contentLtx)
        f = open('tmp/tmpS.html','r')
        s = ''
        for line in f:
            s += line
        self.contentHtml = s
        f.close() 
        subprocess.call('rm tmp/*.*',shell=True)
        super(Article, self).save(*args, **kwargs)
        

class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
   
    def __str__(self):
        return self.title
   
class Answer(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.OneToOneField(Question)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.content
