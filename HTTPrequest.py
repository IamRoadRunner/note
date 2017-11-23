Handling HTTP requests

urlpatterns = [
	url(r'^articlers/([0-9]{4})/([0-9]{2})/([0-9]+)/$',views.article_detail),
]
#会顺序匹配，捕获小括号中的值并且作为位置参数传给后边的函数比如/articlers/2005/03/02 
#views.article_detail(request,'2005','03','02')

url(r'^articlers/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]+)/$',views.article_detail),
#捕获的参数作为关键字参数传进去。
#views.article_detail(request,year='2005',month='03',day='02')

#匹配是不包括GET POST请求方式的参数和域名
http://www.example.com/myapp/ URLconf 将查找myappp/
http://www.example.com/myapp/?page=3 仍然查找myapp/

捕获的参数都是字符串


Specifying defaults for view arguments

in app/views.py
def fun(request,arg='xxx')
	...
#如果不捕获参数的模式匹配，默认参数会传进去；如果捕获参数的模式匹配，将捕获的参数传进去

在根urlconf里设置错误处理


from django.conf.urls import url,include

url(r'^community/',include('django_website.app_name.urls'))
#当遇到include时 把匹配到的部分去掉，将剩余的部分传给include里边的urlconf

extra_patterns = [
    url(r'^reports/(?P<id>[0-9]+)/$', credit_views.report),
    url(r'^charge/$', credit_views.charge),
]

urlpatterns = [
    url(r'^$', main_views.homepage),
    url(r'^help/', include('apps.help.urls')),
    url(r'^credit/', include(extra_patterns)),
]
/credit/reports/ will be handled by the credit_views.report()


include 可以用来声明共同路径前缀一次，后面的部分分组
urlpatterns = [
	#共同的路径前缀
	url(r'^(?P<page_slug>[\w-]+)-(?P<page_id>\w+)/', include([
		url(r'^history/$', views.history),
		url(r'^edit/$', views.edit),
		url(r'^discuss/$', views.discuss),
		url(r'^permissions/$', views.permissions),
	])),
]

捕获的参数会传到include中的URLconf里

urlpatterns = [
    url(r'blog/(page-(\d+)/)?$', blog_articles),                  # bad
    url(r'comments/(?:page-(?P<page_number>\d+)/)?$', comments),  # good
]
blog/page-2 将匹配blog_articles 两个位置参数page-2/ 和2
comments/page-2 将匹配comment 带有一个值为2的关键字参数,(?:..)是外围不捕获参数

Passing extra options to view functions

url(r'^articlers/([0-9]{4})/$',views.article_detail,name='',{'foo':'bar'}),

dictions will be passed to views.article_detail(request,year='2005',foo='bar')
#捕获的参数和传入的字典可能名称相同，使用字典的名称
#可以用相同的方式传递字典到include中的URLconf，但是会传到每一个url里

Url reverse

django 提供URL映射作为URL设计的唯一存储库，使用URLconf填充他，双向使用
1.根据用户/浏览器的url请求调用相应的视图，提取相应的参数
2.根据django视图和将要传递的参数的值，获取相关联的URL，叫做反向解析URL

使用反向解析
#在模板中，使用url模板标签 
在url(正则,view.fun(),name='') 
模板里边使用{% url 'name' variable %}
#在python代码中使用reverse()
from django.urls import reverse
return HttpResponseRedirect(reverse('name',args=(variable,)))
#在更高层中使用get_absolute_url()


#in addition to URL name,use the same name,reverse() matches the number of arguments 
#and the names of the keyword arguments

命名空间
应用命名空间，正在部署的应用，他的每个实例有相同的命令空间
实例命名空间，在项目中是唯一的，实例命名空间可以和应用命名空间相同，表示应用的默认实例

使用':'指定，sports:polls:index  polls在sports的命名空间，index在polls的命名空间中

polls(这个是应用名):index

先匹配应用命名空间，polls的，返回实例列表
通过rquest.current_app 设置当前应用实例
如果没有当前实例，django会查找默认实例
如果没有默认实例django会挑选最后一个部署的实例
如果没有匹配应用命名空间，django将尝试对此命名空间作一个实例命名空间查找

如果使用author-polls:index 将会匹配具体的

application namespaces can be specified in two ways

1.app_name = ''在urlpatterns之前指定，使用的时候在include('app_name.urls')
2.在urlpatterns 中include另一个some_patterns=([url(name='instancename'),url(),'app_name'])
(<list of url() instances>,<application namespace>)

#不指定instancename就会使用默认的namespace(和应用命名空间相同的名)
#the instance namespace can be specified using the namespace argument to include()

Write views

from django.http import HttpResponse 

def foo(request):
	return HttpResponse()

Returning errors

request/response有一些子类对应不同的返回状态码
比如，HttpResponseNotFound('<>html<>')
但是可以自己把状态码返回一个HttpResponse(status=200)

The Http404 exception

django.http.Http404
DEBUG set False ,404 can be  served

View decorator

from django.view.decorators.http import decorator

@require_http_methods(["",""])
指定view可以使用的request methods(GET,POST)

@require_GET()
@require_POST()
@require_safe() the view only accepts the GET and HEAD(只请求页面的首部) methods


File uploads
当django在处理文件上传的时候，文件数据被保存在request.FILES(FILES是个字典)

from django import forms
class UploadFileForm(forms.Form):
	file = forms.FileField()
处理这个表单的视图会在request中接收到上传的数据

#can be accessible as request.FILES['file'] ,and this only contain data if
#the request method was POST and the <form> that posted the request has the attribute
#enctype="multipart/form-data"


def handle_uplcoaded_file(f):
	with open('some/file/name.txt'.'wb+') as destination:
		for chunk in f.chunks():#使用chunks不用read()避免大文件占用过多的内存
			destination.write(chunk)
#在构造form的时候pass request.FIlES ,这样file data bound into a form 			
form = UploadFileForm(request.Post,request.FILES)#视图向表单发送数据
if form is_valid():
	form.save()

也可以手动构造一个对象可以简单的这样赋值给模型
instance = ModelWithFileField(request.FILES['file'])
instance.save()

ins = handle_uplcoaded_file(request.FILES['file'])
ins.save()

Uploading mulitiple files 

class FileFieldForm(forms.Form):
	file_field = form.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

#then override the post method of your FormView subclass
from django.views.generic.edit import FormView
calss FileFieldView(FormView):
	form_class = FileFieldForm
	template_name = ''
	success_url = ''

	def post(self,request,*args,**kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')
		if form.is_valid():
			for i in files:
				do something
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

FILE_UPLOAD_HANDLERS
	["django.core.files.uploadhandler.MemoryFileUploadHandler",
	"django.core.files.uploadhandler.TemporaryFileUploadHandler"]

#读小文件在内存里，大的在硬盘

Where uploaded data is stored

小于2.5M的在内存里，内存里读，硬盘里写，很快
比较大时，就把上传文件写在系统临时文件目录中，

modify upload handlers on the fly

在request.POST或者request.FIlES之前修改
modifying request.upload_handlers()
#this list will contain the upload handlers given by FILE_UPLOAD_HANDLERS
#but you can modify

上传过程中向某类ajax空间提供反馈
request.upload_handlers.insert(0, ProgressBarUploadHandler())
request.upload_handlers = [ProgressBarUploadHandler()] #完全替换上传处理器

@csrf_exempt来允许修改上传处理器
在真正处理请求的函数上使用@csrf_protect
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def upload_file_view(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler())
    return _upload_file_view(request)

@csrf_protect
def _upload_file_view(request):
    ... # Process request
处理器可能在csrf验证完成之前开始接受上传文件


Shortcut functions

from django.shorcuts import render

render(
	request(必选用于生成response),
	template_name(必选,完整名称或名称序列),
	[context] 上下文字典 默认为空 渲染之前调用
	[context_instance]
	[content_type] use for the resulting document default the value DEFAULT_CONTENT_TYPE
	[status] status code for the response defaults to 200
	[current_app]当前正在渲染的实例
	[dirs]
	[using]the Name of a template engine to use for loading the template
)
结合给定的模板和上下文字典 返回选然后的HttpReaponse对象
from django.http import HttpResponse
from django.template import loader

t = loader.get_template('')
c = {'':''}
return HttpResponse(t.render(c,request),content_type='')
#same as
from django.shortcuts import render

return render(request,'template',{'':''},content_type='')

render_to_response(
	template_name
	context
	content
	content_type 
	status
	using
)#不推荐的这种

redirect(
	to
	permanent=Ture/False #永久或临时重定向
	*args 
	**kwargs
)#renturn an HttpResponseRedirect 
redirect()

Redirect(
	1.by passing some object
	2.by passing the name of a view  and optionally some arguments
	3.by passing URL /some/usl/ or 'http://example.com/'
	,permanent=True 
)

get_object_or_404(klass,*args,**kwargs)

#calls get() on a given model manager, but it raise Http404 instead of the model's DoesNotExist
#klass 是一个Model class ,Manager or a QuerySet inistance from which to get the object
#**kwargs lookup parameters which shoud be in the format accepted by get() and filter()

def my_view(request):
	my_object = get_object_or_404(MyModel,pk=1)

#same as

def my_view(request):
	try:
		my_object = MyModel.objects.get(pk=1)
	except MyModel.DoesNotExist:
		raise Http404("  ")

get_list_or_404(klass,*args,**kwargs)
#return the result of filter() on a given model manager cast to a list,raising Http404 if empty

Generic views

View
class django.views.generic.base.View
can be imported from django.views

	from django.http import HttpResponse
	from django.views import View

	class MyView(View):
	    
	    def get(self,request,*args,**kwargs):
		return HttpResponse('xxx')

	from django.conf.urls import url
	from myapp.views import MyView

	urlpatterns=[
	    url(r'^mine/$',MyView.as_view(),name='my-view'),
	]

Attributes
	http_method_names
	default:
	['get','post','put','patch','delete','head','options','trace']

Methods
classmethod as_view(**initkwargs) 
	Returns a callable view that takes a request and return a response
	response = MyView.as_view()(request) the return view has view_class and view_initkwargs attributes

dispatch(request,*args,**kwargs)
	the view part of the view ,the method accepts a request arguement  plus arguments
	and returns a HTTP response
	会检查HTTP 方法，使用method来匹配HTTP method,GET被get()匹配，POST被post()匹配其他的相同
	默认的HEAD请求被get()匹配
http_method_not_allowed(request,*args,**kwargs)
	默认安装启用之后返回HTTPResponseNotAllowed 一个被允许的方法的列表。

options(request,*args,**kwargs)
	handles responding to request for the OPTIONS HTTP verb.返回一个响应，头包含一个
	被允许的HTTP方法的名字列表。
TemplateView
	class django.views.generic.base.TemplateView
	渲染所给的模板，使用URL中包含的上下文变量
	urlpatterns=[usl(r'^$',PageView.as_view(),template_name='xxx/xxx')]

RedirectView
class django.views.generic.base.RedirectView

class Exam(RedirectView):
    Attrubutes
    url=重定向到的url,as string,如果是None raise 410
    pattern_name=重定向的URL pattern的名字 
    permanent=whether the redirect should be permanent.如果是True状态码返回301，如果为False状态码为302.
    默认的为False
    query_string=如果为True，query string 就会被添加到URL，如果为False默认False
    Methods
    get_redirect_url(*args,**kwargs)
    结构化重定向目标的URL， 
重定向到给定的URL，
url(xxx,RedirectView.as_view(url:'http://'))




JsonResponse
	JsonResponse.__init__(data,encoder=DjangoJSONEncoder,safe=True,**kwargs)
	HttpResponse的一个子类，用户帮助创建JSON编码的响应，从父类集成大部分行为
	data参数为一个dict实例，如果safe参数设置为False,它可以是任何JSON序列
	encoder 用于序列化data,有默认DjangoJSONEncoder
	safe默认为True如果设置为False，可以传递任何对象进行序列化，如果为True第一个参数就应该为dict

	from django.http import JsonResponse
	response = JsonResponse({'foo':'bar'})
	response.content



Middleware
是一个钩子框架，介入django的请求和响应过程，用于在全局修改django的输入和输出

#middleware is a callable that takes a request and return a response,like view

def simple_middleware(get_response):
#one-time configuration and init
	def middleware(request):
		#code to be executed for each request before
		response = get_response(request)
		return response
	return middleware 
#same as
class f(object):
	def __init__(self,get_response):#不能添加别的参数 be called once when the web server starts
		self.get_response = get_response()
	def __call__(self,request):
		response = self.get_response(request)
		return response
#each request calls get_response to pass the request in to the next layer(the middleware)
#the response will then pass through erery layer(the middleware in reverse order) on the way back out

process_view(request,view_func,view_args,view_kwargs)
is called before django calls the view
return None(will execute other process_view moddleware  then the appropriate view) 
or
HttpResponse(it will apply response middleware to that HttpResponse and return the result )

process_exception(request(a HttpResponse object),exception(是一个被视图函数中方法抛出来的exception对象))
抛出异常时调用这个中间件返回None或HttpResponse 对象

process_template_response(request(HttpRequest object),response(TemplateResponse object,django视图或中间件返回))
必须返回一个实现了render方法的响应对象
能修改所给的response通过response.template_name response.context_data

模板中间件被调用完，响应会自动被渲染,不用手动render

Streaming response
StreamingHttpResponse 没有content 属性，中间件不能按原来的处理
需要测试streaming responses

if response.streaming:
	response.streaming_content = wrap_streaming_content(response.streaming_content)
else:
	response.content = alter_content(response.content)

#假设streaming_content 很大，内存盛不下
def wrap_streaming_content(content):
	for chunk in content:
		yield alter_content(chunk)

210

Sessions

setting.py 'django.contrib.sessions.middleware.SessionMiddleware'
by default django stores sessions in database setting : django.contrib.sessions.models.Session 

use a database-backed session need to add 'django.contrib.sessions' to INSTALLED_APPS
AND migrate

using cached sessions
django.contrib.sessions.backends.cache 
#session 数据会被直接存储到缓存  缓存会被收回，当缓存重新开始

set SESSION_ENGINE to 'django.contrib.sessions.backends.cached_db'
#同时存进缓存和数据库中，缓存没有了直接使用数据库中的数据

using file_base sessions
set the SESSION_ENGINE "django.contrib.sessions.backends.file"
SESSION_FILE_PATH to control where django stores session fiiles 

using cookie-based sessions
set the SESSION_ENGINE to "django.contrib.sessions.backends.signed_cookies"

#推荐设置SESSION_COOKIE_HTTPONLY = True 阻止js访问stored data


Using sessions in views

when SessionMiddleware is achivated the first argument to any django view will
have a session attribute

class backends.base.SessionBase

	__getitem__(key)
	exa: fav_color = request.session['fav_color']
	__setitem__(key,value)
	exa:request.session['fav_color'] = 'blue'
	__delitm__(key)
	exa:del request.session['fav_color']#key 没在session里的话提示错误
	__contains__(key)
	 'fav_color' in request.session
	get(key,default=None)
	fav_color = request.session.get('fav_color','red')
	213
	flush()#删除会话数据和会话cookie django.contrib.auth.logout() calls it
	set_test_cookie()
	set_expity(value)设置session终止时间
	request.session.set_expiry(300) make the session expire in 5 minutes
	#计算时间是按最后一次 session was modified
	get_expiry_age()
	#返回session终止的秒数如果是浏览器关闭session失效，这个时间等于SESSION_COOKIE_AGE
	clear_expired() #从session store清除终止session called by clearsessions
	cycle_key()#创建新的session key while retaining the current session data.
	django.contrib.auth.login() calls this

Session serialization

use the SESSION_SERILIZER settion to customize the session serialization format

#serializers.JSONSerializer 序列化string ksys only
request.session[0] = 'bar'
request.session['0']
'bar'

def logout(request):
	try:
		del request.session['member_id']
	except KeyError:
		pass
	return HttpResponse("You're logged out")

Setting test cookies 

在一个视图中调用request.session.set_test_cookie()并在接下来的视图中调用test_cookie_worked()
使用delete_test_cookie()来清除测试的cookie

导入SessionStore对象，
from importlib import  import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

也可以 
from django.contrib.sessions.backends.db import SessionStore
s = SessionStore(session_key='')
s.save()

from django.contrub.sessions.models import Session 
s =  Session.objects.get(pk='')
s.expire_data 返回终止日期
s.(使用)get_decoded()获取会话字典
字典是以编码后的格式保存的

会话何时保存
默认是会话被修改时才会保存到数据库中

request.session['foo']['bar'] = 'baz'
这种情况需要设置request.session.modified = True 告诉会话对象它被修改过了

cookie 只有会话被创建或是被修改才会发送
SESSION_SAVE_EVERY_REQUEST为True 会话的cookie将在每个请求中发送

响应状态码500会话不被保存

浏览器时长会话和永久会话
SESSION_EXPIRE_AT_BROWSER_CLOSE 默认为False 有一个时长SESSION_COOKIE_AGE
如果设置为Ture浏览器关闭就失效

using the database backend 定期清理会话 clearsessions 
cache backend(sutomaticlly delete data ) and cookie backend don't need(stored by the browsers) 

The SessionStore object

exists()
create()
save()
delete()
load()
clear_expired()
AbstractBaseSession and BaseSessionManager are importable 
django.contrib.sessions.base_session

class base_session.AbstractBaseSession
	the abstract base session model
	session_key
	session_date
	expire_data
	classmethod get_session_store_class()
		return a session store class to be used with session model
	get_decoded()
		decoding is performed by the session store class 

class base_session.BaseSessionManager
	encode
		return the given session dictionary serialized and encoded as a string 
		decoding is performed by the session store class tied to a model class 

	save()

class backends.db.SessionStore
	classmethod get_model_class()
		override this method to return a custom session model if you need one 
	create_model_instance(data)
		return a new instance of the session model object which represents the current session state 
		you can modify session model data before it is saved to database 

class backends.cached_db.SessionStore
	cache_key_prefix
	add a prefix to build a cache key string
 
 migrating from build-in cached_db to custom one based on cached_db you shoud
 in order to prevent a namespace clash:
 class SessionStore(CacheDBStore):
 	cache_key_prefix = 'mysessions.custom_cached_db_backend'
