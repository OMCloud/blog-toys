# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

#app_name告诉django这个urls属于哪个应用
#视图函数命令空间
app_name = 'Blog'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    #使用类视图的url写法
    url(r'^$', views.IndexView.as_view(), name='index'), #文章首页列表

    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'), #文章详情

    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'), #文章归档

    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'), #文章分类

    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'), #文章标签

    # url(r'^search/$', views.search, name='search'), #全文搜索
]