HTML forms

a form is collection of elements inside <form>..</form> 
send that information back to the server

一个表单必须有目的地(响应用户输入数据的url)和方式(发送数据使用的HTTP方法)
处理表单时只会用到GET POST
登陆表单使用post 浏览器组合表单数据编码传输 发送到服务器 接受响应

get提交数据为字符串 使用它生成url(这个url包含数据发送地址和数据键值)

Forms in Django
可能是指HTML<form> 生成它的django的Form 或者提交发送的结构化数据 或这些的部分或和

Form 类描述一个表单并决定他如何工作和展现
表单类的字段会映射到html的<input>表单元素
表单字段本身也是类，他们管理表单数据并在表单提交时验证
每个字段都有一个合适的默认的widget类 需要是可以覆盖

render an object in Django
1.get hold of it in the view 
2.pass it to the template context
3.expand it to html markup using template variable

在视图中实例一个表单
可以让他为空也可以填充他
1从保存的模型实例获得数据
2从其他源整理的数据
3从前边的html表单提交的数据

Building a form

<form action="/告诉浏览器表单数据发送到哪里/" method="post">
    <label for="your_name">Your name:</label>#可以到form里定义label
    <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
    <input type="submit" value="OK">
</form>  

from django import forms
class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name',max_length=100(阻止用户输入过长，验证输入长度))

Form的实例有is_valid()方法，为所有字段运行验证，都合法返回True，把表单数据放到cleaned_data属性中

views
from .forms import NameForm
def get_name(request):
	if request.method == 'POST':
		form = NameForm(request.POST)#使用请求数据填充，绑定数据至表单
		if form.is_valid():
			#也可以在数据确定去向之前更新数据库或做其他处理
			#return HttpResponstRdirect('告诉浏览器重定向到哪')
			return redirect('//')
	else:
		form = NameForm()#如果是一个GET请求，会创建一个空表单实例，初次访问URL时的情况
	return render(request,'name.html',{'form':form})

More about django form 

未绑定(渲染给用户时为空或包含默认的值)与绑定(绑定的表单具有提交的数据，可以进行验证)
is_bound() True/False

Form fields

CharField,EmailField.BooleanField
IntegerField,FloatField

Widgets
CharField have a TextInput widget >> <input type="text ">
message = forms.CharField(label='内容',widget=forms.Textarea)

表单提交的数据通过了is_valid() 数据会位于form.cleaned_data字典中
但是依然可以从request.POST 直接访问到未验证的数据

Wroking with form templates

将表单实例放进模板的上下文 {{ form }}将正确的渲染<label><input>元素
但是表单输出不包含<form> <submit>
输出选项{{ form.as_table(tr)/as_p(p)/as_ul(li) }}

每个字段都是表单的一个属性，{{ form.name_of_field }}访问
完整的<label>元素可以使用label_tag()生成{{ form.subject.label_tag }}

{{ form.name_of_field.errors }}在头部就会显示渲染的错误列表
可迭代显示{% for error in form.name_of_field.errors %}{% endfor %}

非字段错误会显示另外的类比如nonfield

Looping over the form`s fields

{% for field in form %}
	<div>
		{{ field.errors }}
		{% if field.help_text %}
		<p>{{ field.help_text|safe }}</p>
		{{% endif %}}
{% endfor %}

{{ field.laberl }}the label of the field
field.label_tag  包含在<label>标签中的字段Label label_suffix  ":"
field.id_for_label  用于这个字段的id 例子中的id_email
<label for="id_email">Email address:</label>
field.value  the value of the field
field.html_name 
field.errors  输出一个<ul class="errorlist"> 包含字段的验证错误信息
field.is_hidden 判断是否为隐藏字段

Looping over hidden and visible fields

{% for hidden in form.hidden_fields %}
{% for visible in form.visible_fields %}

reusable form templates

#in your form template:
{% include "form_snippet.html" %}

#in form_snippet.html
{% for field in form %}
	<div>
		{{ field.errors}}
		{{ field.label_tag }} {{ field }}
	</div>
{% endfor %}

可以使用with参数对表单对象起个别名
{% include"form_snippet.html" with form=comment_form %}


Formsets

from django import forms
class ArticleForm(forms.Form):
	title = forms.CharField()
	pub_date = forms.DateField()
一次创建多个Article 使用ArticleForm创建一个表单集

from django.forms import formset_factory
ArticleFormSet = formset_factory(ArticleForm,extra=#控制显示的表单数目)	

可以迭代表单集中的表单
formset = ArticleFormSet()
for form in formset:
	print(form.as_table)
以创建时的顺序渲染表单，__iter__()可以改变顺序

formset = ArticleFormSet(initial=[
	{'title':'django is ...',
	'pub_data':datetime.date.today(),}
])

max_num= to limit the number of forms the formset will display

max_num如果比存在的初始数据条目多的话extra会被添加
如果初始化数据条目超过了max_num 初始化数据表单会忽略max_num限制，extra表单不显示
它只影响表单的数目展示，不影响验证
validate_max=True 传给了 formset_factory() max_num 才会影响验证

Formset validation

data ={
	'key':'value'
}
 formset = ArticleFormSet(data)
 formset.is_valid()
 
#each field in a formset`s forms may include HTML sttributes such as maxlength
#form fields of formsets won`t include the required attribute 
True/False
formset.errors是一个列表
formset.total_error_count()错误条数

check if form data differs from the initial data 
formset.has_changed()
True/False

the management form is available as an attribute of the formset itself.
when rendering a formset in a template, you can include all the management
data by rendering {{ my_formset.management_form }}

total_form_count and initial_form_count

BaseFormSet  has a couple of methods(total_form_count and initial_form_count) closely 
related to the ManagementForm 

total_form_count returns the total number of forms in this formset
initial_form_count returns the number of forms in the formset that were pre-filled
and to determine how many forms are required.

empty_form
returns a form instance with a prefix of __prefix__ 

Custom format valudation

a formset has a clean method which is to define your own valudation that works at the formset level

# from django.forms import BaseFormSet
# class BaseArticleFormSet(BaseFormSet):
# 	def clean(self):
# 		pass自己编写检测函数
ArticleFormSet = formset_factory(ArticleForm,formset=BaseArticleFormSet)
data = {}

formset = ArticleFormSet(data)
formset.is_valid()

the formset clean method is called after all the Form.clean methods have been called
formset.non_form_errors() will found the errors

Valudation the number of forms in a formset

Validation_max
validate_max = True is passsed to formset_factory() valudation will check the number of forms
in the data set

minus those marked for deletion, is less than or equal to max_num

ArticleFormSet = formset_factory(ArticleForm,max_num=1,validate_max=True)
validate_max=True 验证 max_num 严格，即使initial data超出了max_num规定的长度，使其失效

不顾validate_max 如果表单数量超过max_num 1000那么一千之外的不会再检验，保证不受大量post请求攻击
 
Validate_min
is greater than or equal to min_num

Dealing with ordering and deletion of forms

the formset_factory()provide  can_order and can_delete
to help with ordering and deletion of forms from a formset

can_order  formset.orderde_forms
default:False
from django.forms import formset_factory
from myapp.forms import ArticleForm
ArticleFormSet = formset_factory(ArticleForm,can_order=True)
formset = ArticleFormSet(initial=[
	{'title':'Article #1','pub_date':datatime.data(2004,5,26)}
	{'title':'Article #2','pub_date':datatime.data(2004,5,27)}
])
for form in formset:
	print(form.as_table())

for form in formset.ordered_forms:
	print(form.cleande_data)


它会生成一个新的兼做ORDER的字段是一个forms.IntegerField

can_delete  formset.deleted_objects
default:False
this adds a new field to eache form named DELETE  is a forms.BooleanField
[form.cleande_data for form in formset.deleted_forms]

if you use ModelFormSet the model instance for deleted forms will be deleted 
when you call formset.save()

instance = formset.save(commit=False)#object will not be deleted automatically
for obj in formset.deleted_objects:
	obj.delete() #to actually delete them

Adding additional fields to a formset
there is a method named add_fields 重写添加字段或重新定义字段/属性 of the order and deletion fields

from django.forms import BaseFormSet
from django.forms import formset_factory
from myapp.forms import ArticleForm 

class BaseArticleFormSet(BaseFormSet):
	def add_fields(self,form,index):
		super(BaseArticleFormSet,self).add_fields(form,index)
		form.fields["my_field"] = forms.CharField()
		#增加了一个字段

ArticleFormSet = formset_factory(ArticleForm,formset=BaseArticleFormSet)


Passing custom parameters to formset forms when instantiating the formset
class MyArticleForm(ArticleForm):
	def __init__(self,*args,**kwargs):#重写父类的__init__方法
		self.user = kwargs.pop('user')
		super(MyArticleForm,self).__init__(*args,**kwargs)
		通过super实例化的代理对象调用父类的同名方法
		#pass MyArticleForm when instantiating the formset
ArticleFormSet = formset_factory(MyArticleForm)
formset = ArticleFormSet(form_kwargs={'user':request.user})

the formset base class provide a get_form_kwargs method
the method takes a signle argument (the index of the form in the formset)
None for the empty_form

Using a formset in views and templates

from django.forms import formset_factory
from django.shorcuts import render
from myapp.forms import ArticleForm

def manage_articles(request):
	ArticleFormSet = formset_factory(ArticleForm)
	if request.method == 'POST':
		formset = ArticleFormSet(request.POST,request.FILES)
		if formset.is_valid():
			pass
	else:
		formset = ArticleFormSet()
	return render(request,'manage_atticles.html',{'formset':formset})

{{ formset.management_form }}#渲染所有的表单

<table>
	{{ formset }}
	ends up calling the as_table method on the formset class

Manually rendered can_delete and can_order
render can_delete parmeter with {{ form.DELETE }}
{% if formset.can_delete %}
{{ form.DELETE }}
{{% endif %}}

{{ form.ORDER }}

Using more than one formset in a view
article_formset = ArticleFormSet(request.POST,request.FILES,prefix='articles')

Creating forms from models 

ModelForm
#从django的模型创建表单
from django.forms import ModelForm 
from myapp.models import Article 

class ArticleForm(ModelForm):
	class Meta:
		model = Article 
		fields = ['pub_date','headline','content','reporter']

form = ArticleForm()
article = Article.objects.get(pk=1)
form = ArticleForm(instance=article)

foreignkey > django.forms.ModelChoiceField
#他是一个ChoiceField，他的选项是模型的查询集

manytomanyfield > django.forms.ModelMultipleChoiceField 
#他是一个MultipleChoiceField

模型字段设置blank=True 那么表单字段的required设置为False
表单字段的label设置为模型字段的verbose_naem第一个字母大写
如果模型字段设置了choices那么表单字段的widget将设置成select
其选项来自模型字段的choices，
example
from django.db import models
from django.forms import ModelForm

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']

same as:

from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=3,
                widget=forms.Select(choices=TITLE_CHOICES))
    birth_date = forms.DateField(required=False)

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())

validation on a ModelForm

validating the form 
validating the model instance

模型表单的验证在调用is_valid()或访问errors之后隐式调用
或者通过full_clean()显示的调用

模型验证Model.full_clean()在表单验证这一步内部触发，紧跟在表单的clean()方法调用之后

cleaning process modifies the model instance passed to the ModelForm constructor in various
ways,don`t reuse it

Overriding the clean() method to provide additional validation 
模型表单实例包含一个instance属性表示与他绑定的模型实例
ModelFrom.clean()方法设置一个标识符，使模型验证这一步验证标记为unique，unique_together
unique_for_date|month|yeaer的模型字段的唯一性

与模型验证的交互

模型表单将调用与表单字段对应的每个模型字段的clean()方法，已经排除的字段不再进行验证
模型的clean()方法在唯一性检验之前调用


模型error_messages注意事项

表单字段级别或表单级别的错误信息比模型字段级别的错误信息优先
模型字段的错误信息只用于模型验证步骤引发的validationerror的时候

覆盖错误信息
form django.core.exceptons import NON_FIELD_ERRORS
class ArticleForm(ModelForm):
	class Meta:
		error_messages = {
			NON_FIELD_ERRORS:{
				'unique_together': "%(model_name)s's %(field_labels)s are not unique."
			}
		}

Save() method

every ModelForm has a save() method.
creates or saves a database object from the data bound to the form 
如果没有会创建，如果存在会更新
example
#create a form instance from post data
f = ArticleForm(request.POST)

#save a new Article objet from the form's data
new_article = f.save()

a = Article.objects.get(pk=1)
f = ArticleForm(request.POST,instance=a)#既有post又有instance按post，用于修改具体的信息
f.save()
如果表单没有验证，使用save()时将检查form.errors来验证。
a ValueError will be raised if the data in the form doesn`t validate
save()接收一个commit参数为 True/False 默认为True,如果为False那么将返回一个没有保存到数据库的
对象，你还需要调用返回的模型实例的save(),保存之前定义一些处理可以这么用

commit=False 时 django不会立即为多对多关系保存表单数据。因为只有实例在数据库中存在
的时候才可以保存实例的多对多数据
f = AuthorForm(request.POST)
new_author = f.save(commit=False)
new_author.some_field = 'some_value'
new_author.save()
f.save_m2m()保存多对多数据

使用save_m2m()保存多对多的表单数据，只有你使用commit=False时才需要
当你只是用save()，所有的data包括多对多的data都会被保存

Selecting the fields to use 

设置表单中要使用的字段或除去某些不用的字段
class AuthorForm(ModelForm):
	model = Author
	fields = '__all__'使用所有字段
	exclude = ['title']排除某个字段
	字段出现的顺序和在模型中定义的顺序一致，多对多出现在最后
如果设置模型字段的editable=False 那么从该模型创建的任何表单都不会包含该字段

如果设置了有字段不被包含进表单，那么该字段也不会被表单的save()保存 ，如果手动添加这些字段到表单中
他们也不会从模型实例初始化。
缺省字段不能为空，要提供默认值，或commit=False 再进行手动设置所需要的字段

Overriding the default fields

to dpecify a custom widget for a field ,use the widgets attribute of the inner Meta class 
be a dictionary mapping field names to widget classes or instances
<textarea> instead of its default<input typt="text">

class AuthorForm(ModelForm):
	class Meta:
		model = Author
		fields = ('name','title','birth_date')
		widgets = {
			'name':Textarea(attrs={'cols':80,'rows':20}),
		}

and
labels = {
	'name':_('Writer'),
}
help_texts = {
	'name':_('Some useful help text.'),
}
error_messages = {
	'name':{
		'max_length':_("this write's name is too long."),
	}
}
他们只适用自动生成的字段

使用指定类
field_classes = {
	'slug':MySlugFormField,
}


complete control over of a field

#指定验证
class ArticleForm(ModelForm):
	slug = CharField(validators=[validate_slug])

ModelForm 自动成成相应字段的Form 取决于Meta 的fields 属性和在ModelForm中显式声明的字段
ModelForm 只生成表单中没有的字段

Enabling localization of fields 
使用localized_fields属性启用字段的本地化功能

class Meta:
	model = Author
	localized_fields = ('birth_date',)
设置为__all__ 所有字段将会本地化

Form inheritance
表单继承
class EnhancedArticleForm(ArticleForm):
	def clean_pub_date(self):
		..

继承Meta 并重写
class RestrictedArticleForm(EnhancedArticleForm):
	class Meta(ArticleForm.Meta):
		exclude = ('body',)

多个基类有Meta 继承时使用第一个

如果从Form and ModelForm继承，确保ModelForm 在MRO里第一个出现
因为这些类依赖不同的元类，而一个类只能有一个元类

在子类上将名称设置为None，声明删除继承的Field

provide initial values

article = Article.objects.get(pk=1)
form = ArticleForm(initial={'name':'wz'},instance=article)
form['headlinle'].value()

ModelFome factory function

create forms from the standalone function modelform_factory()

from django.forms.models import modelform_factory
from myapp.models import Book
BookForm = modelform_factory(Book,fields=("author","title"))
#代替使用类定义来从模型创建表单

对已有表单类做简单修改
from django.forms import Textarea
Form = modelform_factory(Book,form=BookForm,
						widget={"title":Textarea()})
Form = modelform_factory(Author,form=AuthorForm,localized_fields=
	("birth_date",))

Model formsets

class models.BaseModelFormSet

from django.forms.models import modelformset_factory
AuthorFormSet = modelformset_factory(Author,fields=('name','title'))
formset = AuthorFormSet()
print(formset)

modelformset_factory()使用formset_factory()生成表单集

Changing the queryset

formset = AuthorFormSet(queryset=Author.objects.filter(name__startswith='o')/none())
或者是创建子类设置self.queryset in __init__

from django.forms.models import BaseModelFormSet
class BaseAuthorFormSet(BaseModelFormSet):
	def __init__(self,*args,**kwargs):
		super(BaseAuthorFormSet,self).__init__(*args,**kwargs)
		self.queryset = Author.objects.filter(name__startswit='o')
AuthorFormSet = modelformset_factory(Author,fields=('name','title'),formset=BaseAuthorFormSet)

Changing the form
当使用modelformset_factory时,modelform_factory()将会创建一个模型
class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ('name','title')
	def clean_naem(self):
		pass

将模型作为参数传递过去
AuthorFormSet = modelformset_factory(Author,form=AuthorForm)

modelformset_factory 有几个参数，可以传给modelform_factory

指定要在widgets中使用的小部件
AuthorFormSet = modelformset_factory(Author,fields=('',''),widget={'name':Textarea(attra={'':xx})})

字段启用本地化
AuthorFormSet = modelformset_factory(Author,fields=('',''),localized_fields=(''))

initial 能为表单集中的表单指定初始数据，模型表单集中初始数据仅应用在增加的表单中，
不会应用到已存在的模型实例

保存表单集中的对象
作为ModelForm保存数据到模型对象
formset = AuthorFormSet(request.POST)
instance = formset.save() #instance 是列表
save()返回已保存到数据库的实例，

使用commit=False 使数据保存到数据库之前将数据附加到实例

Limiting the number of editable objects
max_num extra 控制额外表单的显示数量
max_num 不会限制已经存在的表单对象的显示
max_num 大于存在的关联的对象数量，表单将添加extra个额外的空白表单，只要表单数量不超过max_num

Using a model formset in a view
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from myapp.models import Author

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = AuthorFormSet()
    return render_to_response("manage_authors.html", {
        "formset": formset,
    })

Overriding clean() on a ModelFormSet

ModelFormSet 的clean()验证formset中没有项目违反唯一约束(unique,unique_together,unique_for_date|month|year)
如果重写clean()要调用父类(BaseModelFormSet)的clean()
class f(BaseModelFormSet):
	def clean(self):
		super(f,self).clean()
		for form in self.forms:
要修改ModelFormSet.clean()中的值，需要修改form.instance

for form in self.forms:
	name = form.cleaned_data['name'].upper()
	form.cleaned_data['name'] = name
	form.instance.name = name 

使用自定义的queryset

def manage_authors(request):
    AuthorFormSet = modelformset_factory(Author, fields=('name', 'title'))
    if request.method == 'POST':
        formset = AuthorFormSet(request.POST, request.FILES,
        						queryset=Author.objects.filter(name__startswit='o'))
        if formset.is_valid():
            formset.save()
            # do something.

Using the formset in the template

django模板中有三种方法来渲染表单集
1<form method="post" action="">
	{{ formset }}
 </form>
 #表单集完成大部分工作

2 <form method="post" action="">
	{{ fromset.management_form }}
	{% for form in formset %}
		{{ form }}
	{% endfor %}
 </form>
 #手动渲染formset

3<form method="post" action="">
	{{ fromset.management_form }}
	{% for form in formset %}
		{% for field in form%}
			{{ field.label_tag }} {{ field }}
		{% endfor %}
	{% endfor %}
 </form>



<form method="post" action="">
	{{ fromset.management_form }}
	{% for form in formset %}
		{{ form.id }}
		<ul>
			<li>{{ form.name }}</li>
			<li>{{ form.age }}</li>
		</ul>
	{% endfor %}
</form>
 #手动呈现每个字段

内联Formsets

class models.BaseInlineFormSet
简化通过外键处理相关对象的情况

class Author(models.Model):
	name = models.CharField(max_length=100)

class Book(models.Model):
	author = models.Foreignkey(Author)
	title = models.CharField(max_length=100)

from django.forms.models import inlineformset_factory
BookFormSet = inlineformset_factory(Author,Book,fields=('title',))
author = Author.objects.get(name='Mike')
formset = BookFormSet(instance=author)

覆盖Inlineformset上的方法
需要子类化BaseInlineFormSet 而不是BaseModelFormSet
可以传递参数formset=

多个外键对同一个模型
可以在模型字段中增加related_name=''
BookFormSet = inlineformset_factory(Author,Book,
									fk_name='',
									fields=('title',))

在视图中使用内联格式
def manage_books(request, author_id):
    author = Author.objects.get(pk=author_id)
    BookInlineFormSet = inlineformset_factory(Author, Book, fields=('title',))
    if request.method == "POST":
        formset = BookInlineFormSet(request.POST, request.FILES, instance=author)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(author.get_absolute_url())
    else:
        formset = BookInlineFormSet(instance=author)
    return render_to_response("manage_books.html", {
        "formset": formset,
    })
    #允许用户编辑模型的相关对象传进了author_id，后边传进了instance

inlineformset_factory 使用modelformset_factory 将大部分参数传递给modelformset_factory
可以将widgets传递给modelformset_factory

Form Assets

the widgets that the django admin application uses stored in django.contrib.admin.widgets

static definition
from django import forms
class CalendarWidget(forms.TextInput):
	class Media:
		css = {
			'all':('pretty.css',)
			'tv,projector':('xxx.css')
		}
		js = ('animations.js','actions.js')

#每次CalendarWidget 被用在一个表单上，会包含上述的css和js
这些静态文件作为CalendarWidget的属性
css 可以是多个文件名作为tuple，key值来确定作用于谁
key值可以有多个逗号隔开
<link href="" type="text/css" media="tv,projector" rel="xxx.css"/>
子类会继承父类的widget如果不希望继承添加一个extend = False 

Media as a dynamic property
class CalendarWidget(forms.TextInput)L:
	@property
	def media(self):
		return froms.Media(css={'all':('pretty.css')},
							js=('animations.js','actions.js'))

Paths in asset definitions
if the django.contrib.staticfiles app is installed ,it wil be used to server assets.
STATIC_URL and MEDIA_URL 是必要的当渲染整个网页 django will check if STATIC_URL
setting is not None and automatically fall back to using MEDIA_URL
if the MEDIA_URL was 'http://uploads.example.com/' and STATIC_URL was None

class CalendarWidget(forms.TextInput):
	class Media:
		css = {
			'all':('pretty.css',)
			'tv,projector':('xxx.css')
		}
		js = ('animations.js','actions.js')

class OtherWidget(forms.TextInput):
	class Media:
		js = ('whizbang.js')

w1 = CalendarWidget()
w2 = OtherWidget()

print(w1.media + w2.media)
the result Media object contains the union of the assets specified by both

