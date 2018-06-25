创建users
from django.contrib.auth.models import User
user = User.objects.create_user('','')
user.save()

User.objects.get(username='')
User.set_password('')
save(User)

认证
authenticate(username='',password='')看密码对用户是否有效
权限和授权
test for basic permissions
the model name Bar
应用的app_label是foo和一个名为Bar的模型
user.has_perm('foo.add_bar/foo.change_bar/foo.delete_bar')测试它是否有权限
第一次运行migrage时会将之前安装的模型创建默认的权限

Groups
user and Group  manytomany
在组中的用户会具有组所有的权限
除了权限，组还是给用户分类的方法，给他们某些标签或扩展的功能

用程序创建权限
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
content_type = ContentType.objects.get_for_model(model_name)
permission = Permission.objects.create(codename='can_publish',
					name='',
					content_type=content_thpe)
user_permissions 属性分配给一个User permissions 属性分配给Group

权限的缓存
modelbackend 第一次访问对象来检查权限的时候会缓存他们的权限，但是权限添加进来之后没有立即检查他们，
如果需要立即检查(在测试或试图中)，可以从数据库中获取User
def foo(request,user_id):
	user = get_object_or_404(User,pk=user_id)
	#测试权限
	user.has_perm('myapp.change_bar')
	permission = Permission.objects.get(codename='change_bar')

Web请求中的认证
	request.POST request.FILE
	使用session和middleware来拦截request对象到认证系统中
	请求有一个user属性，request.user表示当前用户，登录之后是User的实例，如果没有登录，该属性值设置成AnonymousUser的一个实例可以使用request.user.is_authenticated:看是否认证

	Log a user in
	fjango.contrib.auth.login()
用户认证，
login(request,user,backend=None)
	from a view,log a user in ,user login(),takes an HttpRequest object and a User object,
	login() saves the user`s id in the session


	from django.contrib.auth import authenticate,login

	def a_view(request):
		username = request.POST['username']
		password = request.POST['password']
		result = authenticate(request,username=username,password=password)
		判断result的值
		if result is not None:
			login(request,result)
	the user`s id and the backend the authentication used are saved in user`s session
	authentication backend 存到seddion中被查找的顺序是：
	使用提供的值，使用user.backend属性的值，使用backend in AUTHENTICATION_BACKENDS
	情况一和二需要.引入backend路径字符串

	Log a user out
logout(request)
	djnago.contrib.auth.logout() it takes an HttpRequest object no return value

	def logout_view(request):
		logout(request)
	如果用户没有登录，使用logout() doesn`t throw any error 
	调用logout() 当前请求的session的数据会被完全清除防止被别人使用

只允许登录的用户访问
	1.原始方法是检查request.user.is_authenticated,重定向到登录界面
	def my_view(request):
		if not request.user.is_authenticated:
			....

	2.login_required 装饰器
	login_required(redirect_field_name='',login_url=None)

	from django.contrib.auth.decorators import login_required
	@login_required
	def my_view(request):
		pass
	如果用户没有登录，重定向到settings.LOGIN_URL,并且传递当前查询字符串中的绝对路径
	如果用户已经登录，那么正常执行视图，
	成功认证后的用户应，该被重定向的路径，存储在查询字符串的"next"的参数中
	@login_required(redirect_field_name='my_redirect_field')使用一个不同的名字
	存储重定向路径的模板上下文变量使用redirect_field_name的值作为他的键而不是next
	@login_required(login_url='')
	如果没指定login_url需要确保setting.LOGIN_URL于登录的视图关联
	from django.contrib.auth import views as auth_views
	url(r'^accounts/login/$',auth_views.login)

	在URLconf中
	from django.contrib.auth import view
	url(r'',view.login)

	The loginRequired
	使用LoginRequiredMixin
	没有认证的用户请求都会重定向到登录界面或显示HTTP403 取决于raise_exception
	from django.contrib.auth.mixins import LoginRequiredMixin
	class myview(LoginRequiredMixin,View):
		login_url = '/login'
		redirect_field_name = 'redirect_name'


给验证登录的用户添加访问权限
	def my_view(request):
	    if not request.user.email.endswith('@xxx')#测试，检查用户的邮件是否是特的那个的地址
		return redirect(xxx)
	@user_passes_test(要求一个以User对象为参数的回调函数)

	@permission_required(perm[])检查一个用户是否有指定的权限

	对普通视图使用权限
	基于类的普通视图可以使用@view_dispatch

认证的视图
	django提供一些视图，来处理的登录登出密码管理等，使用内建的认证表单，也可以使用自己的表单
	但是没有为认证视图提供默认的模板，自己创建要使用的模板

	使用django提供的视图
	urlpatterns = [
	    url('^',include('django.contrib.auth.urls'))
	]
	也可以以指定特定的视图
	视图具有一些可选参数，改变视图的行为
	一种是
	urlpatterns = [
	    url('^','django.contrib.auth.views.password_change',
		{'template_name':'change-password.html'}
		)
	]
	所有的视图都返回一个TemplateResponse实例，所以在渲染前自定义响应很容易。
	另一种是在自己的视图中封装一个视图
from django.contrib.auth import views
def change_password(request):
    template_response = views.password_change(request)
    return template_response

所有的认证视图
	django.contrib.auth.views.login 
	通过GET调用显示一个POST给相同URL的登录表单
	通过POST调用并带有用户提交的凭证，会尝试登录，登录成功会重定向到next中指定的URL，登录不成功会重新显示登录表单
	可以提供html模板给login，默认调用registeration/login.html
		模板会得到四个模板上下文变量：
			form认证表单的表单对象，next，site，site_name
		可以通过参数template_name，将模板传递给视图
url(r'^accounts/login/$',auth_views.login,{'template_name':'myapp/login.html'})

	logout(request[,next_page退出之后要重定向的URL，template_name退出之后要展示的模板的完整名称，
	redirect_field_name,current_app,extra_context])

	logout_then_login(request[,login_url,current_app,extra_context])
	登出一个用户然后重定向到登录页面

	password_change()允许一个用户修改他的密码

	password_change_done(request[,template_name,current_app,extra_context])
	这个页面在用户修改密码之后显示

	password_reset()
	允许用户通过生成一次性的连接并发送到注册的邮箱地址中来重置密码

	password_reset_done()
	这个页面在用户发送重置密码邮件之后显示

	password_reset_confirm()
	为输入新密码展示表单

	redirect_to_login(next[,login_url(重定向到的登录页面的URL),redirect_field_name(包含注销后重定向的URL
	的GET字段的名称，如果传递给定的GET参数，则覆盖next)])
	重定向到登录页面，在登录成功后回到另一个URL(next中的)

内建的表单
	认证系统提供的内建的表单位于django.contrib.auth.forms
	内建的认证表单对它们处理的用户模型做了特定假设
class AdminPasswordChangeForm
class AuthenticationForm
  自定义哪些用户可以登录，使用自定义表单，子类化AuthenticationForm 并覆盖confirm_login_allowed
class PasswordChangeForm
class PasswordResetForm
用于生成并发送邮件重置密码的一个表单


模板中的认证数据
当使用RequestContext时，当前登录的用户和他们的权限在模板上下文中可以访问
用户
  当渲染RequestContext模板时，当前的用户会存储在模板变量{{ user }}中
  只有使用RequestContext模板时，才可以访问模板变量
权限
  登录的用户权限存储在{{ perms }}中，单一属性的查找是User.has_module_perms的代理，有许可{{ perms.foo }}显示True
  二级属性查找是User.has_perm的代理{{ perms.foo.can_vote }}如果有会显示True
  使用{% if %}检查权限 使用{% if 'foo' in perms %}查询权限

在admin中管理用户
	一个帐号有添加用户的权限但是没有权限修改他们，那么该帐号将不能添加用户。安全机制
修改密码
	用户密码不会显示在admin上，但是会显示密码存储细节，这个信息的显示中包含一条指向修改密码表单的连接，允许管理员修改用户密码。

django中的密码管理
	调整PASSWORD_HASHERS中的加密算法的顺序来选择加密存储算法
密码升级
	用户登录之后，如果他们的密码和django中的加密存储算法不同，django会自动将算法升级为首选的那个，
	但是它只会升级在PASSWORD_HASHERS中出现的算法，所以升级到新系统时不要移除列表中的元素。列表中没有的算法，将不会升级
Manually managing a user`s password
	django.contrib.auth.hashers 提供函数创建和验证哈希密码
	check_password(password(要检查的纯文本),encoded(数据库中的))比较纯文本密码和数据库中哈希后的密码来手动验证用户。
	make_password(password,salt=None,hasher='default')创建哈希密码
	is_password_usable(encoded_password)检查提供的字符串是否可以用check_password()验证




自定义用户验证
在底层有一个认证后台列表，django会尝试所有的认证后台进行认证，通过认证就会停止
认证后台通过AUTHENTICATION_BACKENDS 设置指定，是一个python路径的元组，元组顺序很重要
默认情况下('django.contrib.auth.backends.ModelBackend')
他会检查django用户的数据库并查询内建权限，没有限制机制
认证通过后会在用户的session中存储它使用的认证后端，如果重新认证需要清除掉session数据
Session.objects.all().delete()

编写一个认证后端
一个认证后端是个实现两个方法的类：
get_user(user_id)user_id 这个参数是用来表示User，返回一个User对象
authenticate(**credentials)使用username='',passeord=''作为关键字参数，返回User

在定制后端中处理授权
认证后端完成了(get_group_permission(),get_all_permissions(),has_perm(),has_module_perms())
user model 就会给它授予相应的许可
只要任意一个backends授予了一个user权限，django就给这个user权限







































































