from ..models import Post
from ..models import Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-created_time")[0:num]


@register.simple_tag
def archives():
    return Post.objects.dates("created_time", 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()