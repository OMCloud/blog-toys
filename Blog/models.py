from django.db import models

from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    #标题
    title = models.CharField(max_length=70)
    #正文
    body = models.TextField()
    #创建时间
    created_time = models.DateTimeField()
    #修改时间
    modified_time = models.DateTimeField()

    #文章摘要
    #默认字段不能为空， blank=TRUE 允许该字段可以为空
    excerpt = models.CharField(max_length=200, blank=True)
    #文章与分类属于一对多的关系，所有使用ForeignKey
    category = models.ForeignKey(Category)
    #文章与标签属于多对多的关系，所以使用ManyToManyField
    tags = models.ManyToManyField(Tag, blank=True)
    #文章作者，这里User是从django.contrib.auth.models 导入
    #django.contrib.auth 是django内置的应用，专门用于处理网用户的注册、登录等流程，User是django为
    #我们已经实现的用户模型
    #这里通过ForeignKey把文章和User关联起来
    #文章和作者是一对多的关系  和 category类似
    author = models.ForeignKey(User)

    #新增views字段记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            self.excerpt = strip_tags(md.convert(self.body))[:100]
        super(Post, self).save(*args, **kwargs)

