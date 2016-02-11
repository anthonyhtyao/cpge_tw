import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cpge_tw.settings')

import django
django.setup()

from reco.models import UserProfile, Article

def populate():
	yulin = UserProfile.objects.get(name = 'HUANG Yu-Lin')
	huating = UserProfile.objects.get(name = 'YAO Hua-Ting')
	add_article(auteur = yulin, title = 'article created bu yu-lin', content = 'This is the content of article by yulin')
	add_article(auteur = huating, title = 'article created by huating', content = 'This is the content of article by huating')



def add_article(auteur, title, content):
	a = Article.objects.get_or_create(author = auteur, title=title)[0]
	a.content=content
	a.save()
	return a

def test():
	article = Article.objects.get(id=1)
	print(type(article.content))
if __name__=='__main__':
	populate()
	print('Ca marche')