"""cpge_tw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cpge_tw import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^(?P<page>(q_and_a|about|contact){1})/$', views.page, name='page'),
    url(r'^(?P<page>(q_and_a|about|contact){1})/edit$', views.pageEdit, name='pageEdit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^settings$', views.userSettings, name='userSettings'),
    url(r'^download$', views.download, name='download'),
    url(r'^newarticle$', views.newArticle, name='newArticle'),
    url(r'^article/(?P<articleID>[0-9]*)/$',views.article, name='article'),
    url(r'^article/(?P<articleID>[0-9]*)/edit$',views.editArticle, name='editArticle'),
    url(r'^article/(?P<articleID>[0-9]*)/articlecomment$',views.articlecomment, name='articlecomment'),
    url(r'^articlecomment/(?P<commentID>[0-9]*)/(?P<articleID>[0-9]*)/$',views.replycomment, name='replycomment'),
    url(r'^articlelist/$',views.articlelist, name='articlelist'),
    url(r'^questionlist/$',views.questionlist, name='questionlist'),
    url(r'^question/(?P<questionID>[0-9]*)/$', views.answer, name="answer"),
    url(r'^createarticle$',views.createarticle, name='createarticle'),
    url(r'^tinymce/', include('tinymce.urls') ),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^addquestion$', views.addquestion, name='addquestion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
