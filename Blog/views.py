from django.shortcuts import render
import markdown
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category
from Comments.forms import CommentForm

# def index(request):
#     #return HttpResponse("欢迎您！！！")
#     post_list = Post.objects.all()
#     return render(request, 'Blog/index.html', context={
#                     'post_list': post_list
#     })


#使用List类视图
class IndexView(ListView):
    model = Post
    template_name = 'Blog/index.html'
    context_object_name = 'post_list'


def archives(request, year, month):
    '''
    根据日期获取归档文件
    :param request: 
    :param year: 
    :param month: 
    :return: 
    '''
    post_list = Post.objects.all().filter(created_time__year=year,
                                          created_time__month=month)
    return render(request, 'Blog/index.html', context={'post_list': post_list})


class ArchivesView(ListView):
    model = Post
    template_name = "Blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")

        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                        created_time__month=month)


class CategoryView(ListView):
    model = Post
    template_name = "Blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)


# def category(request, pk):
#     #注册Category类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.all().filter(category=cate)
#     return render(request, 'Blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    #阅读量增加1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ]
                         )

    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {'post':post,
               'form': form,
               'comment_list': comment_list
               }


    return render(request, 'Blog/detail.html', context= context)

class PostDetailView(DetailView):
    model = Post
    template_name = "Blog/detail.html"
    context_object_name = "post"


    def get(self, request, *args, **kwargs):
        #get方法会返回一个HttpResponse实例
        #只有先调用父类的get方法，能够有self.object属性，其值为Post模型实例
        #即被访问的文章post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        #将文章阅读量加1
        self.object.increase_views()

        return response


    def get_object(self, queryset=None):
        #重写get_object 方法的目的是需要对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions =[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post



    def get_context_data(self, **kwargs):

        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        }
        )

        return context
