filter(**kwargs)
exclude(**kwargs)
get(**kwargs)

exact 
startswith
endswith
contains
icontains#忽略大小写

id_exact=id=pk
Entry.objects.filter(blog__id__exact=3)
=Entry.objects.filter(blog__id=3)
=Entry.objects.filter(blog__pk=3)

Blog.objects.firlter(pk__in=[1,4,7])

F object
django.db.models.F

#where the author's name is the same as the blog name
Entry.objects.filter(authors__name=F('blog__name'))

from datetime import timedelta
Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))


Entry.objects.filter(headline__contains='%')
=SELECT ... WHERE headline LIKE '%\%%';
%表示多字符通配符
_表示单字符通配符

Caching
queryset = Entry.objects.all()
print([p.headline for p in queryset])
print([p.pub_date for p in queryset])
#缓存，查询一次会有记录可以多次使用。

#repeatedly getting a certain index in a queryset 
#object will query the database each time
queryset = Entry.object.all()
print(queryset[5])
print(queryset[5])#queries the database twice

but
queryset = Entry.object.all()
[entry for entry in queryset]#queries the database
print(queryset[5])#uses cache
print(queryset[5])#uses cache

bool(queryset)
list[queryset]

Q object for colplex lookups
django.db.models.Q
used to encapsulate a collection of keywoed arguements

from django.db.models import Q
Q(question__startswith='What')
Q objects can ber combined using the & and | 

Q(question__startswith='Who') | Q(question__startswith='what')
=WHERE question LIKE 'Who%' OR question LIKE 'What%'

negated using the ~ operator
Q(question__startswith='Who')| ~Q(pub_date__year=2005)

Poll.objects.get(
	Q(question__startswith='Who'),
	Q(pub_date=date(2005,5,2)) | Q(pub_date=date(2005,5,6))
)

SELECT * FORM polls WHERE question LIKE 'Who%'
		AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

#可以和关键字参数一起使用，如果有Q对象，关键字参数必须在
#Q对象之后。

Comparing objects

equals sign:==
some_entry == other_entry

comparisons will always use the primary key
if your primary key is called name 
some_obj == other_obj
=some_obj.name == other_obj.name 

Deleting objects

#Queryset has a delete() method,delete objects in bulk
Entry.objects.filter(pub_date__year=2005).delete()
#this deletes all Entry objects eith a pub_date year of 2005

.
will be deleted along with it .

b = Blog.objects.get(pk=1)
b.delete()
#this will delete the Blog and all of its Entry objects.
#this cascade behavior via on_delete arguements to the ForeighKey..

if you do want to delete all the objects ,
then you have to explicitly request a complete query set 
Entry.objects.all().delete()

Copying model instances


entry = Entry.objects.all([0])

 detail = EntryDetail.objects.all()[0]
 detail.pk = None
 detail.entry = entry
 detail.save()

Updating multiple objects at once

Entry.objects.filter(pub_date__year=2007).update(headline='something')

b = Blog.objects.get(pk=1)
#Change every Entry so that it belongs to this Blog
Entry.objects.all().update(blog=b)

#filter based on related fields, but only update columns in the 
#model's main table
Entry.objects.select_related().filter(blog=b).update(headline='something')

#update one field based on the value of another field in the model.
Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)

#can't  introduce joins when you use F() objects in an update
#you can only reference fields local to the model being updated.
#this will raise a FieldError
Entry.objects.update(headling=F('blog__name'))


Related objects

from django.db import models
class Entry(models.Model):
	blog = models.ForeighKey(Blog,on_delete=models.CASCADE)
	author = models.ManyToManyField(Author)

	class __str__():
		pass

class Blog(models.Model):
	name = models.CharField(max_length=30)

	class __str__():
		pass

class Author(models.Model):
	name = models.CharField(max_length=10)

	class __str__():
		pass

One-to-many relationships

e = Entry.objects.get(id=2)
e.blog# returns the related Blog object

e.blog = some_blog
e.save()

e = Entry.objects.get(id=2)
print(e.blog)#hits the database to retrieve the associated Blog
print(e.blog)#Doesn't hit the database;uses caches version


#select_related used for one-to-one and one-to-many 
e = Entry.objects.select_related().get(id=2)
print(e.blog)#doesn't hit the database;uses cached
print(e.blog)#doesn't hit the database;uses cached

Following relationships "backward"

b = Blog.objects.all(id=1)
b.entry_set.all()

#override the Foo_set name by setting the related_name in the ForeignKey definition
modefy
blog = ForeignKey(
	Blog,
	on_delete=models.CASCADE,#级联删除
	related_name='entries'
) 

b = Blog.objects.all(id=1)
b.entries.all()

Using a custom reverse manager

from django.db import models
class Entry(models.Model):
	objects = models.Manager()#default Manager
	entries = EntryManager()#custom Manager

b = Blog.objects.get(id=1)
b.entry_set(manager='entries').all()

Additional methods to handle related objects

add(obj1,obj2,..)
create(**kwargs)
remove(obj1,obj2,..) #remove the specified model objects from the related object set
clear() #remove all objects from the related object set
set(objs)#replace the set of related objects
b = Blog.objects.get(id=1)
b.entry_set.set([e1,e2])

#each 'reverse' like addition,creation,deletion is immediately and
#automatically saved to the database

Many-to-Many relationships
like ForeighKey

one-to-one relationships

class EntryDetail(models.Model):
	entry = models.OneToOneField(Entry,on_delete=models.CASCADE)
	details = models.TextField()
#like the many-to-one 

#represents a single object,rather than a collection of objects
e = Entry.objects.get(id=2)
e.entrydetail 

Aggregation
from django.db import models
class Author(models.Model):
	name = models.CharField(max_length=100)
	age = models.IntegerField()

class Publisher(models.Model):
	name = models.CharField(max_length=300)
	num_awards = models.IntegerField()

class Book(models.Model):
	name = models.CharField(max_length=300)
	pages = models.IntegerField()
	price = models.DecimalField(max_digits=10,decimal_places=2)
	rating = models.FloatField()
	authors = models.ManyToManyField(Author)
	publisher = models.ForeighKey(Publisher)
	pubdate = models.DateField()

class Store(models.Model):
	name = models.CharField(max_length=300)
	books = models.ManyToManyField(Book)
	registered_users = models.PositiveIntegerField()

Book.objects.count()
Book.objects.filter(publisher__name='xxx').count()

#two ways to generate aggregates
1\
from django.db.models import Avg
Book.objects.all().aggregate(Avg('price'))
{'price__avg': 35.2}

from django.db.models import Max 
Book.objects.all().aggregate(Max('price'))
=Book.objects.aggregate(Avg('price'))
#aggregate return name-value pairs
{'price__max': Decimal('80.20')}

from django.db.models import F,FloatField,Sum

Book.objects.all().aggregate(
	price_per_page=Sum(
		F('price')/F('pages'),
		output_field=FloatField()
	)
)
#{'price_per_page': 0.122245}

2\
from django.db.models import count
pubs = Publisher.objects.annotate(num_books=Count('book'))
#根据Publisher，并计算每组的book的数量赋值给变量num_book，从而添加注解
pubs#显示分组
pubs[0].num_books#显示第一组的book的数量

pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]

#生成多个aggregate
Book.objects.aggregate(Avg('price'),Max('price'),Min('price'))

q = Book.objects.annotate(Count('authors',distinct=True),Count('store',distinct=True))
q[0].authors__count
q[0].store__count

Store.objects.annotate(min_price=Min('books__price'),max_price=Max('books__price'))
Store.objects.aggregate(youngest_age=Min('books__authors__age'))


Publisher.objects.aggregate(oldest_pubdate=Min('book__pubdate'))
default name is book__pubdate__min
Author.objects.annotate(total_pages=Sum('book__pages'))
Author.objects.aggregate(average_rating=Avg('book__rating'))

Use filter

Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))
Book.objects.filter(name__startswith="Django").aggregate(Avg('price'))

Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)
Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
Author.objects.values('name')#指定按照name分组
annotate will return result for each object 
the values() will return the result of each group

Note:the order of the filter and annotate

Order of annotate() and values() clauses

values().annotate() #any annotations will be automatically added to the result set
annotate().values() #you need to explicitly include the aggregate column
 Author.objects.annotate(average_rating=Avg('book__rating')).values('name','average_rating')

Manager

extar manager methods
class someManager(models.Manager):
	def Foo(self):
		pass

class someModel(models.Model):
	objects = someManager()


modify the initial Queryset
#override a Manager's base QuerySet by overrding the Manager.get_queryset()
class DahlBookManager(models.Manager):
	def get_queryset(self):
		return super(DahlBookManager,self).get_queryset().filter(author='Roald Dahl')

class Book(models.Model):
	objects = models.Manager()
	dahl_objects = DahlBookManager()


Book.objects.all()#不变
Book.dahl_objects.all()#return the ones written by Roald Dahl

Model._default_manager
#note:django interprets the first Manager defined in a class as the 'default' Manager
using Meta.default_manager_name

Model._base_manager 
#django uses an instance of this manager class
#when accessing related objects,not the _default_managerl
#it would otherwise be filtered out by the default manager

setting Meta.base_manager_name#to tell the django which class to use

##从Manager中调用自定义的QuerySet
#将一些定义到自定义查询集中的额外方法也在管理器上实现。
class PersonQuerySet(models.QuerySet):
	def authors(self):
		return self.filter(role='A')

	def editors(self):
		return self.filter(role='E')

class PersonManager(models.Manager):
	def get_queryset(self):
		return PersonQuerySet(self.model,using=self._db)

	def authors(self):
		return self.get_queryset().authors()

	def editors(self):
		return self.get_queryset().editors()

#you can call both authors() and editors() from the manager which you defined

class CustomQuerySet(models.QuerySet):
	#available on both Manager and QuerySet
	def public_method(self):
		return 
	#only on QuerySet
	def _private_method(self):
		return
	#only on QuerySet
	def  out_public_method(self):
		return
	out_public_method.queryset_only = True

	#both Manager and QuerySet
	def  _out_public_method(self):
		return
	_out_public_method.queryset_only = False



from_queryset()
class Managername()
class Querysername()

Managerclassname.from_queryset(Questsetclassname)()
#可以在变量中存储生成的类

#管理器继承
1.子类显式定义了管理器，django会把他作为默认管理器
2.子类中没有定义管理器，会继承父类管理器作为默认管理器
3.子类中想添加额为的管理器，但是希望继承自父类的管理器为默认管理器，
  需要定义另一个基类，添加新的管理器，然后继承时将其放在默认管理器
  所在基类之后。


Row

#can use as 
raw('SELECT first AS first_name FROM myapp_table)')

#and dictionary
name_map = {'first':'first_name',.....}
first_person = Person.objects.raw('SELECT * FORM myapp_table',translations=name_map)

#索引访问，索引和切片不是在数据库的层面上进行的，如果有大量的查询对象可以在查询时加上LIMIT 再切片，更高效

Deferring model fields

people = Person.objects.raw('SELECT id ,first_name FROM myapp_person')
for p in people:
	print(p.first_name,#原始查询中访问
		  p.last_name)#需要时访问
#每次原始查询必须包含主键


#可传参数是列表或字典
lname = 'Doe'
Person.objects.raw('SELECT id ,first_name FROM myapp_person WHERE last_name = %s',[lname])
%(key)s #SQLite 不支持字典


#直接使用自定义的SQL
from django.db import connection

with connection.cursor() as cursor:
	cursor.execute()
	row = cursor.fetchone/fetchall()
	return row

from dajngo.db import connections
cursor = connections['dbname'].cursor()

#it return a list
#make it as a dict
def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns,row))
		for row in cursor.fetchall()
	]


Namedtuple
#make it as a tuple
from collectons import namedtuple

def namedtuplefetchall(cursor):
	desc = cursor.description
	nt_result = namedtuple('Result',[col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

with connectin.cursor() as c:
	c.execute()

same sa :

b = connection('dbname')
c = b.cursor()
c.execute()
b.close()


Database transactions


#set ATOMIC_REQUESTE  True,将每个请求包裹在一个事务中
#仍然可以使用@transaction.non_atomic_request(using=)让视图方法运行在事务之外
from django.db import transaction

#装饰器创建具备原子性的代码块，正常运行，会被提交，有异常，将回滚
#如果内嵌同样的代码块的话,即便内部正常，外部代码出现异常，将无法提交到数据库中
@transaction.atomic
def viewfunc(request):
	#代码在transaction里面执行
	do_stuff()


#作为上下文管理器使用
def viewfunc(request):
	#这部分在默认自动提交
	do_stuff()
	#这部分代码在transaction里面执行
	with transaction.atomic():
		do_more_stuff()
#外层atomic以及内部嵌套的transaction.atomic()
# 当进入到最外层的 atomic 代码块时会打开一个事务;
# 当进入到内层atomic代码块时会创建一个保存点;
# 当退出内部块时会释放或回滚保存点;
# 当退出外部块时提交或回退事物。

atomic(using=dbname,savepoint=True)
#最外层savepoint不能设置成False，保证错误时能回滚

#可以在配置文件里设置AUTOCOMMIT为False 关闭django的事务管理。
#这样django将不能自动提交

#be executed after a transaction is successfully committed
transaction.on_commit(func,using=)
 or
transaction.on_commit(lambda: )


#保存点就是内嵌的atomic()块，在一个保存点注册的on_commit()会在外部事务提交后执行
with transaction.atomic()#create new transaction
	transaction.on_commit(foo)

	with transaction.atomic()#create savepoint
		transaction.on_commit(bar)
#外部事务提交完成后执行foo，然后执行bar，保存点回滚之后内部回调函数将不执行
#回调函数执行失败不会导致事务回滚on_commit只在自动提交开启或在atomic()中有效


Multiple database
#settings.py 中DATABASES模仿default定义多数据库的信息
#默认情况下migrate使用default数据库，通过--database=xxx 同步不同的数据库
#django_admin 与migrate相同，一次只操作一个数据库，也可以使用--database来控制使用的数据库

Database Router(.....)

#model类型的对象的读写操作应该使用的数据库
db_for_read/write(model,**hints)
#如果obj1，obj2允许关联则返回True，不允许则..这是存粹的验证操作
allow_relation(obj1,obj2,**hints)
#定义迁移操作是否允许在别名为db的数据库上运行
allow_migrate(db,app_label,model_name=None,**hints)

#hints用于某些操作来传递额外的信息给路由
#由数据库路由接收，用于决定哪个数据库接受一个给定的请求

#设置文件里
#DATABASE_ROUTERS = ['path.to.router1','path.to.router2']

User.objects.using('').get()
user_obj.save(using='')
#多个数据库上受用管理器
User.objects.db_manager('').manager_fun()
#db_manager()返回一个绑定在指定数据上的管理器

Tablespaces

class TablespaceExample(models.Model):
	name = models.CharField(max_length=30,db_index=True,db_tablespae="indexes")
	data = models.CharField(max_length=255,db_index=True)
	edges = models.ManyToManyField(to="self",db_tablespae="indexes")

	class Meta:
		db_tablespae = "tables"

#the index for the name field and the indexes on the manytomany table would be
#stored in the "indexes" tablespace.the data field's index stored in the model tablespace
#"tables" by default
#SQLite and MySQL 不支持 tablespaces


Migrage
makemigrations 创建一个迁移
migrate 执行迁移，撤销和列出迁移状态--name指定迁移文件名称
sqlmigrate 展示迁移的sql语句
