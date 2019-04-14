from django.shortcuts import render
import markdown
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag
from Comments.forms import CommentForm



################# 首页列表视图###################
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

    #通过paginate_by 属性来实现分页， 它的值代表每一页文章的数量
    paginate_by = 2    #指定每页显示两篇文章


    def get_context_data(self, **kwargs):
        '''
        在类视图中如果想给模板传递一个字典变量，则需要先通过get_context_data获得模板变量
        因此在这里复写get_context_data方法
        :param kwargs: 
        :return: 
        '''
        #先获取父类传递给模板的字典变量
        context = super().get_context_data(**kwargs)

        #其实在父类的字典变量中已经包含paginator、page_obj、is_paginated 这三个模板变量
        #其中paginator 是 Paginator 的一个实例，page_obj 是 Page 的一个实例，is_paginated 是一个布尔变量，用于指示是否已分页。
        paginator = context.get("paginator")
        page_obj = context.get("page_obj")
        is_paginated = context.get("is_paginated")

        #调用自定义的paginate_data方法获取分页所需数据
        paginate_data = self.paginate_data(paginator, page_obj, is_paginated)

        #将分页信息更新到context
        context.update(paginate_data)

        #将context内容返回
        return context

    def paginate_data(self, paginator, page_obj, is_paginated):
        '''
        自定义分页数据
        :param paginator: 
        :param page: 
        :param is_paginated: 
        :return: 
        '''
        if not is_paginated:
            #如果没有分页，就直接返回空{}
            return {}

        #当前分页左边连续的页码号
        left_page_num = []

        #当前分页左边连续的页码号
        right_page_num = []

        #标签第一页后是否显示省略号
        first_right_has = False

        # 标签第最后一页后是否显示省略号
        last_left_has = False

        #标记是否要显示第一页，如果当前页左边的连续页码中包含第一页，就不用在显示第一页
        show_first_page = False

        #原因同上
        show_last_page = False

        #获取当前请求的页号
        page_number = page_obj.number
        
        #获取分页后的总页数
        total_pages = paginator.num_pages

        #获得整个分页列表
        page_range = paginator.page_range

        if page_number == 1:
            #如果请求的当前页为1.那么当前页左边就不需要数据

            #如果只想获取当前页后的连续两页，如下
            right_page_num = page_range[page_number:page_number + 2]

            #如果最右边的页码比最后的页码减去1还要小，
            #说明右边的页码和最后一页的页之间还有其它页码，因此需要显示省略号
            if right_page_num[-1] < total_pages - 1:
                last_left_has = True

            if right_page_num[-1] < total_pages:
                show_last_page = True

        elif page_number == total_pages:

            left_page_num = page_range[(page_number -3) if (page_number - 3) > 0 else 0:page_number - 1]

            #如果最左侧页码大于2，则1号页和页码间有省略号
            if left_page_num[0] > 2:
                first_right_has = True

            #如果最左侧页码大于1，则需要显示1号页码
            if left_page_num[0] > 1:
                show_first_page = True
        else:
            left_page_num = page_range[(page_number -3) if (page_number -3) > 0 else 0:page_number - 1]
            right_page_num = page_range[page_number:page_number + 2]

            if right_page_num[-1] < total_pages - 1:
                last_left_has = True
            if right_page_num[-1] < total_pages:
                show_last_page = True

            if left_page_num[0] > 2:
                first_right_has = True
            if left_page_num[0] > 1:
                show_first_page = True

        data = {
            'left_page_num' : left_page_num,
            'right_page_num': right_page_num,
            'first_right_has': first_right_has,
            'last_left_has': last_left_has,
            'show_first_page': show_first_page,
            'show_last_page': show_last_page
        }

        return data


#####################归档视图##########################
# def archives(request, year, month):
#     '''
#     根据日期获取归档文件
#     :param request:
#     :param year:
#     :param month:
#     :return:
#     '''
#     post_list = Post.objects.all().filter(created_time__year=year,
#                                           created_time__month=month)
#     return render(request, 'Blog/index.html', context={'post_list': post_list})


class ArchivesView(ListView):
    model = Post
    template_name = "Blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")

        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                        created_time__month=month)


########################文章分类视图#########################

# def category(request, pk):
#     #注册Category类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.all().filter(category=cate)
#     return render(request, 'Blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = "Blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)


############################文章标签试图##################################
class TagView(ListView):
    model = Post
    template_name = "Blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk = self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tags = tag)

############################文章详情视图###############################

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     #阅读量增加1
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ]
#                          )
#
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#
#     context = {'post':post,
#                'form': form,
#                'comment_list': comment_list
#                }
#
#
#     return render(request, 'Blog/detail.html', context= context)

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
