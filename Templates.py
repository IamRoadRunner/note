django 为加载和渲染模板定义了标准api，
使用模板分三步
配置引擎 每个DjangoTemplates后端实例化一个引擎
将模板代码编译成模板，django.template.loader模块提供函数
根据context渲染模板，render()

加载包括根据给定的标识找到模板然后预处理，通常会编译好放在内存中。
渲染表示使用context数据对模板插入值并返回生成的字符串。

支持模板引擎

配置
	class Engine(下边的变量)
	通过TEMPLATES setting
	实例化enging，所有的参数通过关键字参数传递

	BACKEND是一个指向实现了django模板后端api的模板引擎类的路径
	DIRS定义了一个目录列表模板引擎按列表顺序搜索这些目录来下查找模板源文件
	APP_DIRS告诉模板引擎是否应该进入每个安装的应用中查找模板
	OPTIONS 中包含了backend的具体设置
	context_processors是一个python可调用对象的路径列表用于模板渲染时填充其上下文
		他们接收一个HTTP请求对象作为他们的参数，返回一个字典用于合并到上下文中。
	debug如果为True 模板引擎将保存额外的调试信息。
	loaders是一个模板加载类的一个列表
	string_if_invalid:作为字符串输出，用于无效的变量
	file_charset：用于读取磁盘上的模板文件的字符集default is FILE_CHARSET 

	static Engine.get_default()
	Engine.get_template(template_name,using=None)
	使用给定模板加载并且返回一个Template对象，想指定模板引擎使用using指定
	Engine.select_template(template_name_list,using=None)
	可以提供个性化模板
	Engine.select_template(['story_%s.html'%story.id,'story_detail.html'])
	Engine.from_string(template_code)编译给定的template_code，三个都返回一个Template对象

	导入模板失败，两个error
	exception TemplateDoesNotExist
	没有找到指定的模板
	exception TemplateSyntaxError
	找到模板但是模板内部出现错误

加载模板 
	使用Engine的工厂方法创建Template，setting中的TEMPLATES只定义DjangoTemplates引擎的django项目
	from django.template import Template
	templat = Template("my name is {{ xx }}")接收一个原始的模板代码作为参数，
	系统只解析一次原始模板代码，当创建Template对象的时候。

	模板目录
	DIRS 
	是一个字符串列表，包含模板目录的完整路径[os.path.join(BASE_DIR,'templates')]
	设置APP_DIRS:True，那么INSTALL_APPS中的顺序会很重要，第一次运行的时候会缓存模板存在的目录


渲染上下文
	编译好Template对象，使用上下文渲染它。可以使用不同的上下文多次重新渲染相同的模板。
	class Context(dict):
	from django.template import Context,Template
	template = Template("xxx")(Enging.get_template(template_name,using=''))
	context = Context({'':''})
	template.render(context)
	由get_template和select_template 返回的Template对像必须要有一个render()方法
	Template.render(context=None,request=None)
	通过提供context进行渲染，它是一个dict，如果没提供，引擎将使用空的context
使用Context对象
	from django.template import Context
	c = Context({"foo":"bar"})
	c['foo']调用 
	del c['foo']删除
	c.push()进栈
	c.pop()出栈
	c.update({'':''})
	c.flatten()字典形式取出全部



render_to_string(template_name,context,request,using)
loads a template like get_template() and 立即调用render()
	template_name:the name of the template to load and render
	context:
	request:an optional httprequest that will be available during the template`s rendering process
	using:template enging name
from django.template.loader import render_to_string
rendered = render_to_string('my_template.html',{'foo':'bar'})

render() calls render_to_string() and feeds the result into an httpresponse

use configured engines directly
	from django.template import engines
	django_engine = engines['django']
	template = django_engine.from_string('')

	Built_in backends

	DjangoTemplates engines accept the following OPTIONS:
	 
	autoescape:boolean ,True default,set False if rendering non_html templates
	context_processors:以.为分隔符的python调用路径的列表，在一个template被request
	渲染时，可以被调用产生context数据，take a request object as their argument and
	return a dict of items to be merged into the context


	libraries:a dictionary of labels and dotted python paths of template tag modules 
	to register with the template engines
	OPTIONS = {
		'library':{
			'':'path.to.myapp.tags'
		}
	}
	can be loaded by passing the corresponding dictionary key to the {% load %}
	builtins:

class Jinja2
	BACKEND 设置为django.template.backends.jinja2.Jinja2
	APP_DIRS会去查找jinja2命名的目录中
	OPTIONS中的environment项 是一个带点的python路径，调用它返回Jinja2的环境变量
	default to 'jinja2.Environment'

	django 调用该可调用项并传递其他选项作为关键字参数
	'autoescape'
	loader:
	auto_reload:setting.DEBUG 
	undefined:

	jinja2 可以使用函数as a context processor 
	{{ function(request) }}
	the original use case for adding context processors for jinja2 involved
	making an expensive computation that depends on the request
	needing the result in every template
	using the result multiple times in each template

	jinja2后端不会创建django风格的环境，不知道django的上下文处理器，过滤器和标签
	为了使用django特定的api需要将其配置到环境中。
	form jinja2 import Environment
	from django.contrib.staticfiles.storage import staticfiles_storage
	from django.core.urlresolvers import reverse

the django template language

语法
主要有变量和标签
模板是由context来渲染的。渲染就是将context中的值来替换模板中相应的变量
并执行相关的tags，其他的原样输出。

变量
变量的值是来自context中的输出，类似字典keys到values的映射关系
{{ 变量 }}

context包含{'a':'A','b':'B'}

{{ a }},{{ b }}.
渲染之后是A,B.
字典查询，属性或方法查询和数字索引查询都是通过.来实现的
{{ my_dict.key }}
{{ my_object.attribute }}
{{ my_list.0 }}
如果变量被解析成可调用的，模板会无参数调用它，并使用调用的结果来替代模板的值

标签
标签在渲染过程中提供任意逻辑
{% tag %}
大部分标签都接受参数
{% cysle 'odd' 'even' %}
有一些标签需要开始和结束标签
{% if %}hello,{{ user.username }}.{% endif %}
还有for endfor 

过滤器
{{ name|lower }}将文本转换成小写
可以多个过滤器一起使用
Filters transform the value of variables and tag arguments.
{{ django|title }}
会把每个单词的开头字母变为大写的
有些Filter看起来像参数
{{ my_date|date:"Y-m-d" }}
{{ bio|truncatewords:30 }}显示前三十个词
{{ list|join:"," }}使用逗号去连接一个列表中的元素
{{ value|default:"nothing" }}如果变量为false或空就使用给定的默认值
{{ value|length }}返回value的长度，对字符串个列表都起作用
{{ value|filesizeformat }}将数值格式化为一个易读的状态


注释
{# 注释 #}
{% comment %}
{% endcomment %}

组件
components
this is an overview of the django template language`s apis

engine 

template 

context
django.template.Context holds some metadata and context data 
it is passed to Template.render() for rendering a template

大多是情况下，context数据是在一个普通的字典里传递的，如果HttpRequest有需要
是另外传递的。

loaders
加载器
模板加载器负责定位模板，加载，并且返回模板对象

context processors
接收当前的HttpRequest作为参数，并返回一个字典，该字典包含了将要将要添加到渲染的
context 中的数据
他的主要作用是添加所有的模板context共享的公共数据，而不是在每个视图中重复代码。


CLASS-BASED VIEWS
class-based views provide a way to implement views as python objects instead of functions.




模板继承
创建一个基本的骨架模板，包含站点中全部的元素，定义可以被子模板覆盖的blocks
#！/usr/bin/env python 
子模版
{% extends "base.html" %}
{% block title %}title content{% endblock %}会替换base.html中的相应block
extends 会告诉模板引擎 这个模板集成自哪个模板 处理时首先定位父模板 并使用子模版的
block替换父模板对应的block

常常使用三级结构
创建base.html模板控制整个站点的主要视觉和体验
为站点的每个分支创建一个base_SECTIONNAME.html模板，这些模板都继承自base.html
  包含每部分特有的样式和设计
为每一种页面类型创建独立的模板，这些模板继承对应分支的模板

使代码复用，分支范围内的导航会简单
{% extends %}必须是模板中的第一个标签
base模板中block标签越多越好，子模版不必定义父模板中的所有block
如果模板中冗余代码很多可以考虑将其放进父模板中
如果要获取父模板中的block内容可以使用{{ block.super }}
block可以定义一个名字
一个模板中不能定义多个名字相同的block标签

自动HTML转义
django默认打开变量转义
< &lt 
> &gt 
# " &quot
& %amp
如果不希望数据自动转义可以通过一下方式关闭
{{ data|safe }}关闭独立变量上的自动转义
使用模板代码块,将模板包裹在autoedcape标签中
{% autoescape off %}接受off 和 on 
	hello {{ name }}
{% endautoescape %}
base模板中如果转义关闭了，子模版中使用也会是关闭的


字符串字面值和自动转义
所有字面值字符串在插入模板时都不会带有任何自动转义所以要这样写
{{ data|default:"3 &gt; 2" }}

访问方法调用
对象上的方法调用可以用于模板中，
{% for comment in task.comment_set.all %}
	{{ comment }}
{% endfor %}

{{ task.comment_set.all.count }}
也可以访问定义在模型中的方法
class Task(models.Model):
	def foo(self):
		return "bar"
{{ task.foo }}
不能在模板中传递参数来调用方法，数据应该在视图中处理，然后传给模板展示

自定义标签和过滤器库

应用提供自定义的标签和过滤器库，要在模板中访问他们，确保应用在INSTALL_APPS中
例如添加了'django.contrib.humanize'(humanize标签库)之后在模板中使用load标签
{% load humanize %}
{{ xxx|xxx }}
load可以接受多个标签库空格分隔

自定义库和模板继承
加载标签或过滤器库时只在当前模板中有效，不是任何父模板和子模版中都有效


内置标签参考指南

autoescape自动转义将内用转义成HTML输出，等同于将escape作用于每个变量

block 可以被子模版覆盖

comment 注释{% comment[可选的记录注释掉的原因等] %}{% endcomment %}
  此标签不能嵌套使用

csrf_token用于跨站请求伪造 保护

cycle这个标签在循环中很有用,每访问一次依次返回一个元素，最后一个之后返回第一个
	{% for i in range(2) %}
	{% cycle 'row1' 'row2' %}
	{% endfor %}
	可以使用变量，或者混合使用变量和字符串，包含在cycle中的变量会被转义，可以禁止
	使用别名{% cycle 'row1' 'row2' as rowcolors %}使用别名作为一个模板变量进行引入
	{% for i in range(2) %}
	{% cycle 'row1' 'row2' as rowcolors  %}
	{% rowcolors %}
	{% cycle rowcolors %}
	{% endfor %}
	被引号包含的认为是可迭代字符串，没有引号的值当作模板变量
	{% cycle 'row1' 'row2' as rowcolors silent %}
	<tr class="{{ rowcolors }}">{% include "su.html" %}</tr>
	{% endfor %}子模版可以在上下文中访问rowcolors

debug输出整个调试信息，包括当前上下文和导入的模块

filters多个过滤器|连接可以有参数
	{% filter xxx|lower %}
	 bulabula
	{% endfilter %}

firstof输出第一个不为False参数
	{% firstof var1|safe var2 var3 "提供一个字符串防止所有的变量都是False" %}它相当于多个if语句

|first/last第一个/最后一个
|random随机返回一个

for
	循环组中的每个项目

for...empty
在for中没有找到或者是空的时候{% empty %}<>xxxx<>

if  else endif 
运算符==,!=,<,>, in,not in,
过滤器可以在if表达式中使用
复合表达式or,and,not,and优先级高于or

ifchanged检查一个值是否在上一次迭代中改变

ifequal如果给定的两个参数是相等的就显示被标签包含的内容
{% ifequal 1,2 %}{% endifequal %}
1,2可以是变量或给定的字符串

ifnotequal

include加载模板并以标签内的参数渲染，引入别的模板的方法
{% include template_name %} 包括包含在变量template_name中的模板的内容
包含的模板在包含他的模板处被渲染
{% include "name.html" %}
name.html模板
{{ greeting }}{{ person|default:"friend" }}z

也可以使用关键字参数传递
{% include "name.html" with person=" " greeting=" "[only表示仅使用提供的变量] %}
include是一种将子模版渲染并嵌入HTML中的变种方法，子模版不共享父模板状态，子模版独立
block模块在包含之前就被渲染，没有block模块会被include引入并执行。

load加载自定义模板标签集
可以使用from从库中选择性加载单个过滤器或标记

lorem
{% lorem[count][method w for words, p for html,b for plain-text paragraph blocks][random] %}

now显示最近的日期或事件
{% now "js F Y H:i" %}
{% now "DATE_FORMAT/DATETIME_FORMAT/SHORT_DATE_FORMAT/SHORT_DATETIME_FORMA" %}
也可以使用别名，as xxx存储输出在后边使用

regroup
分组
{% regroup cities|dictsort:"country"(排序) by country as country_list %}根据国家将城市分组
{% for country in country_list %}
	{{ country.grouper }}grouper(分组的项目这里是国家)
	country.list (这个群组中所有的项目列表这里是城市)
with使用一个简单的名字缓存一个复杂的变量
url返回一个绝对路径的引用(不包含域名的URL)
verbatim停止模板引擎在该标签中的渲染

过滤器
slice返回列表的一部分slice:"#"
rjust:"#"右对齐给定宽度字段中的值
join 连接列表
dictsort给一个键名进行排序
default
default_if_none
date给定格式对一个date变量格式化
cut移除value中所有的与给出的变量相同的字符串
center 使value在给定的宽度范围内居中
add把add后的参数加给value
linenumbers显示行号
make_list
stringformat根据参数格式化变量
time根据给定的格式格式化时间{{ value|time:"TIME_FORMAT" }}
timesince
timeuntil
title 使字符以大写字符开头其余为小写
truncatechars给一个字符数量，多余的会被截断以...结尾
truncatewords
upper
urlize将文字中的网址和电子邮件地址转换为可点击的链接
wordcount
wordwrap 以指定的行长度换行单词

static
连接保存在STATIC_ROOT中的静态文件
{% load static %}
<img src="{% static "images/hi.jpg" %}" alt="hi!"/>

其他标签和过滤器库
django.contrib.humanize
django.contrib.webdesign
通过在INSTALLED_APPS设置来激活他们

django.contrib.humanize
{% load humanize %}
他的过滤器
apnumber对于数字1-9返回英文拼写
intcomma正数转换成字符串，三位一个逗号
intword大整数转换为适合阅读的形式
naturaltime更人性化的日期格式
ordinal将正数转换为他的序数词字符串

自定义模板标签和过滤器
自定义的标签和过滤器须位于某个应用中，与应用绑定在一起，
应用需要包含templatetages目录，和views.py位于同一级别目录下，创建__init__.py 文件
自定义的标签和过滤器放在templatetags目录下的一个模块里，模块名字就是将来要载入的名字

模块中顶端
from django import template
register = template.Library()所有的标签个过滤器都在其中注册。

编写自定义模板过滤器
其实就是带有参数的python函数{{ var|foo:"bar" }}
变量var和参数bar,大多数过滤器不带参数
def foo(value,arg):
	return value....

注册自定义过滤器
register.filter('foo'过滤器名称,foo编译的函数)
或
@register.filter(name='foo')不声明name将默认使用函数名
def foo(value,arg):
	return ...

期望字符串的过滤器
from django.template.defaultfilters import stringfilter
会将value转换成字符串
@stringfilter

过滤器和自动转义
原始字符串输出时，如果自动转移生效则自动转义，否则保持不变
	在注册过滤器的时候@register.filter(is_safe=True)标记为安全的，默认为false,强制返回字符串
安全字符串，输出时已经被标记为安全，不需要进一步转义
标记为需要转义的字符串，在输出时始终转义


@register.filter(needs_autoeacape=True告诉过滤器函数要传递autoescape关键字)
def foo(value,autoescape=True):启动自动转义
django内置过滤器默认情况下具有autoescape=True

过滤器和时区
如果编写操作datetime对象的自定义过滤器 注册时要将expects_localtime=True
如果过滤器第一个参数是时区相关的日期时间值，django会将它先转换为当前时区

编写自定义模板标签
simple_tag 是Library()的一个方法，接受任意数目的参数的函数
	@register.simple_tag
	它会检查参数的数量，会把参数的引号去掉，如果是模板变量，传递给我们的是变量的值为不是变量本身

	如果模板标签要访问上下文，可以在注册时使用takes_context=True，就不需要传递参数给这个模板标签
	可以在注册时提供自定义名称和filter一样
	{% name 任意数量的由空格分隔的参数 %}
inclusion_tag标签
	@register.inclusion_tag('template_name',takes_context=True)
	def foo(context):第一个参数必须叫做context
赋值标签
	assignment_tag函数，它将标签结果存储到指定的上下文变量中而不是将其输出
	使用as var_name,将结果存储在模板变量中
	如果使用上下文注册时takes_context=True 

高级
模板编译时被拆分成节点，每个节点是django.template.Node的实例，调用他的render()来渲染。
指定标签如何被转换成一个node，以及该节点的render()方法会进行的渲染动作

写编译函数



