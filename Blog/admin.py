from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

#自定义admin管理后台
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_time", "modified_time", "category", "author"]

#把新增的postadmin注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

