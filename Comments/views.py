from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk)

    if request.method == 'POST':

        #利用用户提交的表单请求构造CommentForm实例，Django自动生成表单
        form = CommentForm(request.POST)

        #自动检测表单的合法性
        if form.is_valid():

            #commit=False 作用是仅仅利用表单的数据生成Comment模型类实例，
            #但还不保存评论数据到数据库
            comment = form.save(commit=False)

            #将评论与被评论的文章关联起来
            comment.post = post

            #最终将评论数据保存至数据库
            comment.save()
            #重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，
            # 它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            #如果检测到数据不合法，则重新渲染详情页面，并且渲染表单的错误
            #因此需要传递三个模板变量
            #这里使用的post.comment_set.all()类似于post.objects.all()
            #作用是获取这个文章下的所用评论，
            #原因是post和comment是foreignKey的关系，通过反向查询获取评论
            comment_list = post.comment_set.all() #反向查询，等同于 comment.objects.filter(post=post)
            context = {"post": post,
                       "form": form,
                       "comment_list":comment_list}
            return render(request, "Blog/detail.html", context= context)

    return redirect(post)

