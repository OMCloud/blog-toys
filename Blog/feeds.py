from django.contrib.syndication.views import Feed

from .models import Post

class AllPostRssFeed(Feed):

    #显示在聚合阅读器的标题
    title = "OMCloud的博客"

    #通过聚合阅读器跳转到的网站地址
    link = "/"

    #显示在聚合阅读器上的描述信息
    description = "OMCloud的博客"

    #需要显示的内容条目
    def items(self):
        return Post.objects.all()

    #聚合阅读器中显示的内容条目标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    #聚合阅读器中显示的内容条目描述
    def item_description(self, item):
        return item.body