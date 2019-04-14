from ..models import Post
from ..models import Category
from ..models import Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-created_time")[0:num]


@register.simple_tag
def archives():
    return Post.objects.dates("created_time", 'month', order='DESC')

@register.simple_tag
def get_categories():
    #通过django.db.models.aggregates import Count 来计算分类下的文章数量
    #通过模型名称实现计数
    #return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    #通过django.db.models.aggregates import Count 来计算分类下的文章数量
    #通过模型名称实现计数
    #return Category.objects.all()
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)