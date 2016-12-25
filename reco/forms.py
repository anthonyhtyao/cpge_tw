from django import forms
from django.contrib.auth.models import User
from reco.models import *
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('blog', 'name', 'ispublic', 'highschool', 'prepa', 'grandsecole')

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length = 128)
    contentLtx = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ('title', 'contentLtx')
        #exclude = ["user"]

class CommentForm(forms.ModelForm):
    content = forms.CharField()
    name = forms.CharField(max_length = 128, required=False)
    
    class Meta:
        model = Comment
        fields = ('content', 'name',)

class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length = 128)
    content = forms.CharField()

    class Meta:
        model = Question
        fields = ('title','content')

class AnswerForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Answer
        fields = ('content',)
