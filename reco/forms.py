from django import forms
from django.contrib.auth.models import User
from reco.models import UserProfile, Article, Comment
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('blog', 'name',)

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length = 128)
    content = forms.CharField(widget = TinyMCE(attrs={'cols': 80, 'rows': 3}))

    class Meta:
        model = Article
        fields = ('title', 'content')
        #exclude = ["user"]

class CommentForm(forms.ModelForm):
    content = forms.CharField()
    name = forms.CharField(max_length = 128, required=False)
    
    class Meta:
        model = Comment
        fields = ('content', 'name',)

