from django.conf.urls import url

from . import  views

app_name = "Comments"

urlpatterns = [
    url(r'comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comments'),
]