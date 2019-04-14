一个非常简单的小博客，周末两天没事用来练习一下django的使用。

## 开发所依赖的基础库环境

Python==3.7.0

Django==1.10.6

Markdown==3.1

Pygments==2.3.1

pytz==2018.9

sqlparse==0.3.0

这个小博客系统非常简单，数据直接使用的是django自带的sqlite数据库

## 安装部署注意事项：

#### 打开 settings.py 文件，找到 DEBUG 和 ALLOWED_HOSTS 这两个选项，将它们设置成如下的值：

Mysite/settings.py
```python
...
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '192.168.1.1', '.domain.com']
...
```
修改ALLOWED_HOSTS，指定允许访问的主机地址或者域名

#### 安装依赖
项目还会依赖一些第三方的 Python 库，全部依赖已经写入一个叫 requirements.txt 的文本文件中。
pip install -r requirements.txt

### 收集静态文件

为了方便部署和管理，一般需要把项目中的全部静态文件收集到一个统一的目录下，这个目录通常位于 Django 项目的根目录，并且命名为 static。
已经在settings.py 文件添加了如下内容：
Mysite/settings.py
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
只需要在部署前先执行一下 
python manage.py collectstatic

### 创建数据库文件
需要生成数据库文件
python manage.py migrate

### 创建系统用户
为了方便我们进入 Django 管理后台，我们可以先创建一个管理用户
python manage.py createsuperuser

### 启动项目
python manage.py runserver

如果正常输出如下信息：
Performing system checks...

System check identified no issues (0 silenced).
April 14, 2019 - 13:29:01
Django version 1.10.6, using settings 'MySite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
说明项目正常启动了

这是就可以通过http://127.0.0.1:8000/访问项目了。
