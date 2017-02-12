from django import forms
from reco.models import *
from tinymce.widgets import TinyMCE


class ArticleForm(forms.ModelForm):
    pdf = forms.FileField()
    title = forms.CharField(max_length = 128)
    abstract = forms.CharField(widget=forms.Textarea, required=False)
    contentLtx = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ('pdf','title', 'abstract', 'contentLtx')
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
