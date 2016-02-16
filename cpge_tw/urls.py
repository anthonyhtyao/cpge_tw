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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^article/(?P<articleID>[0-9]*)/$',views.article, name='article'),
    url(r'^article/(?P<articleID>[0-9]*)/edit$',views.editarticle, name='editarticle'),
    url(r'^article/(?P<articleID>[0-9]*)/articlecomment$',views.articlecomment, name='articlecomment'),
    url(r'^articlelist$',views.articlelist, name='articlelist'),
    url(r'^createarticle$',views.createarticle, name='createarticle'),
    url(r'^tinymce/', include('tinymce.urls') ),
    url(r'^logout/$', views.user_logout, name='logout'),
]
