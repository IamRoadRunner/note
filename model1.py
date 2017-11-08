models.OneToOneField(
    place, on_delete=models.CASECADE,
    parent_link=True,
)


class Place(models.Model):
    pass


class Restaurant(Place):
    pass

 1628  cd /var/lib/dpkg/
 1629  ls
 1630  sudo mv info/ info_old
 1631  ls
 1632  mkdir info
 1633  sudo mkdir info
 1634  sudo apt-get update
 1635  sudo apt-get -f install
 1636  sudo mv info/* info_old/
 1637  sudo rm -rf info/
 1638  sudo mv info_old info
 1639  ls
 1640  sudo apt-get --reinstall install `dpkg --get-selections | grep '[[:space:]]install' | cut -f1`
 1641  sudo apt-get -f install

sudo dpkg -i name.deb
sudo apt-get install -f

import random
import string
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 生成验证码
def gene_code():
    width, height = (100, 30)
    bgcolor = tuple(random.sample(range(100, 255), 3))
    fontcolor = (0, 0, 255)
    image = Image.new('RGBA', (width, height), bgcolor)
    font = '/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-R.ttf'
    font = ImageFont.truetype(font=font, size=25)
    draw = ImageDraw.Draw(image)
    # 文本
    source = list(string.ascii_lowercase + '1234567890')
    text = ''.join(random.sample(source, 6))
    # 干扰线
    linecolor = (0,0,0)
    for i in range(0, 4):
        draw.line([(random.randint(0, width), random.randint(0, height)), (random.randint(
            0, width), random.randint(0, height))], fill=linecolor)
    # 干扰点
    chance = min (100, max (0, 2))
    for w in range (width):
        for h in range (height):
            tmp = random.randint (0, 100)
            if tmp > 100 - chance:
                draw.point ((w, h), fill=(0, 0, 0))
    # 填充
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / 6, (height - font_height) / 6), text,
              font=font, fill=fontcolor)
    # 扭曲
    image = image.transform((width + 20, height + 10),
                            Image.AFFINE, (0.8, 0, 0, 0, 0.8, 0), Image.BILINEAR)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image

return super(classname, self).funname()


定义manage命令，新建management/commands/name.py

Manager
管理器
使用people=models.Manager()
重命名管理器

自定义管理器
1.向管理器类中添加额外的方法
2.修改管理器返回的查询集
(通过重写manager.get_queryset())
class PersonManager(model.Manage):
    def get_queryset(self):
        return super(PersonManager,self).get_queryset().filter(xx)

cursor.connection.cursor()
cursor.execute('''

        ''')
管理器方法可以通过self.model来得到它所属的模型类

在一个模型中可以添加多个管理器

从Manager中调用自定义的QuerySet

class PersonQuerySet(model.QuerySet):
    def authors(self):
    def:

class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

class Person(models.Model):
    .
    .
    people = PersonManger()

使用QuerySet的方法创建Manager
QuerySet.as_manager()可以创建一个带有自定义查询集方法副本的管理器实例

创建自定义管理器和一个自定义查询集。
调用Manager.from_queryset()返回管理器的一个子类,带有自定义查询集所有
方法副本


如果类中显式定义了默认管理器，django就会以此作为默认管理器，
否则会从第一个抽象基类中继承默认管理器。

使用基类中的管理器为默认管理器，但是要添加其它管理器，那么就新定义
一个管理器，然后继承。

事务
try:
    with transaction.atomic():
        generate_relationships()(如果出错，执行下边的操作，此处回滚)
except:
    handle_exception()

捕捉数据库异常应该基于atomic代码块来做，

django.db.transaction中
get_autocommit(using=None)
set_autocommit(autocommit,using=None)
using参数的值是数据库的名字，如果没有提供，将会使用'default'

atomic()代码处于活跃状态时，django会拒绝将autocommit从on的状态调整为off，它会
破坏原子性。

事务
事务是一系列数据库语句的原子集。数据库可以确保事务集中的变更要么提交要么会滚。
在django.db.transaction 中有commit，roolback
当atomic()程序块在运行状态，提交和回滚是自动的。

保存点
savepoint()
创建一个新的保存点
savepoint_commit()
释放保存点sid，
savepoint_rollback()
会滚事务保存点sid
clean_savepoints()
重置用来生成唯一保存点id的计数器

@transaction.atomic
def viewfunc(request):
    a.save()
    sid=transaction.savepoint()
    b.save()
    if want_to_keep_b:
        transaction.savepoint_commit(sid)
    else:
        transaction.savepoint_rollback(sid)

聚合

from django.db.models import Avg,Max
Book.objects.all().aggregate(Avg('price'))(all()可以去掉)
{'print__avg':##}
Book.objects.aggregate(average_price=Avg('price'))
{'average_price':##}
聚合的时候可以是多个参数。返回一个结果。

为查询集的每一项生成聚合，返回一个查询集，还可以继续过滤
pubs=Publisher.objects.annotate(num_books=Count('book'))
pubs[0].num_books

连接和聚合
使用'__'表示关联关系

遵循反向关系
Book外键到Publisher
Publisher.objects.annotate(Count('book'))
QuerySet结果中每一个Publisher都包含一个属性book__count

如果values()子句在annotate()子句之前，注解会被自动添加到结果集中，但是
....之后，需要显式包含聚合列。
根据values()子句中的字段对结果进行唯一分组

编写自定义model字段

编写一个类
class Hand(object):
    def __init__(self,north,east,south,west):
        self.north=north
        ...
example=MyModel.objects.get(pk=1)
print(example.hand.north)

new_hand=Hand(north,east,south,west)
example.hand=new_hand
example.save()

后台原理
对象先转换格式来适应数据库中的数据类型

字段类
django字段类不是model的属性，字段类存储在Meta类中，字段类提供了在属性值和
存储在数据库中或发送到serizlizer之间进行转换的机制。
自定义字段的时候
1，用户操作的python对象，分配给模型属性，用于读取显示上边的Hand类
2，field子类，用于转换

编写字段子类
from django.db import models
class HandField(models.Field):
    def __init__(self,*args,**kwargs):
        kwargs['max_length']=104
        super(HandField,self).__init__(*args,**kwargs)

多数据库
在setting中通过DATABASE设置完成，
DATABASE={
        'default':{

            },
        'user':{
            
            }
        }
没有默认那么default字典置空

同步数据库
migrate --database=name

数据库路由
db_for _read(model,**hints)
建议model类型的对象读操作应该使用的数据库

db_for_write()
allow_relation(obj1,obj2,**hints)
如果obj1和obj2之间允许关联则返回True，防止关联返回False，无法判断则返回None
这是验证操作。

allow_migrate(db,app_label,model_name=None,**hints)
定义迁移操作是否允许在别名为db的数据库上运行
hints用于某些操作来传递额外的信息给路由

hints(提示)
hints由数据库路由接受，用于决定那个数据库应该接受一个给定的请求

使用路由
使用DATABASE_ROUTERS设置安装，
一个例子
DATABASES = {
            'auth_db': {
                    'NAME': 'auth_db',
                    'ENGINE': 'django.db.backends.mysql',
                    'USER': 'mysql_user',
                    'PASSWORD': 'swordfish',
                        },
            'primary': {
                    'NAME': 'primary',
                    'ENGINE': 'django.db.backends.mysql',
                    'USER': 'mysql_user',
                    'PASSWORD': 'spam',
                                                        },
            'replica1': {
                    'NAME': 'replica1',
                    'ENGINE': 'django.db.backends.mysql',
                    'USER': 'mysql_user',
                    'PASSWORD': 'eggs',
                        },
            'replica2': {
                    'NAME': 'replica2',
                    'ENGINE': 'django.db.backends.mysql',
                    'USER': 'mysql_user',
                    'PASSWORD': 'bacon',
                    },
            }
现在我们将需要处理路由。首先，我们需要一个路由，它知道发送auth 应用的查询到auth_db：
class AuthRouter(object):
    """
     A router to control all database operations on models in the
    auth application.
     """
    def db_for_read(self, model, **hints):
    """
    Attempts to read auth models go to auth_db.
    """
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
     """
     Attempts to write auth models go to auth_db.
     """
        if model._meta.app_label == 'auth':
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
    Allow relations if a model in the auth app is involved.
    """
        if obj1._meta.app_label == 'auth' or \
                  obj2._meta.app_label == 'auth':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
    """
    Make sure the auth app only appears in the 'auth_db'
    database.
    """
        if app_label == 'auth':
            return db == 'auth_db'
        return None

另一个路由，它发送其它应用的查询到primary/replica(随机)

class PrimaryReplicaRouter(object):
    def db_for_read(self, model, **hints):
     """
     Reads go to a randomly-chosen replica.
     """
        return random.choice(['replica1', 'replica2'])
                                            
    def db_for_write(self, model, **hints):
    """
     Writes always go to primary.
     """
        return 'primary'
    def allow_relation(self, obj1, obj2, **hints):
     """
     Relations between objects are allowed if both objects are
    in the primary/replica pool.
    """
        db_list = ('primary', 'replica1', 'replica2')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None
    def allow_migrate(self, db, app_label, model=None, **hints):
     """
     All non-auth models end up in this pool.
    """
        return True

最后，在设置文件中，我们添加如下内容（替换path.to.为该路由定义所在的真正路径）：
DATABASE_ROUTERS = ['path.to.AuthRouter', 'path.to.PrimaryReplicaRouter']
按列表中的顺序进行

手动选择一个数据库
model.objects.using('name').all()
model.objects.all()使用的是default数据库

save(using='name')
p=Person(name='Fred')
p.save(using='first')
p.pk=None
p.save(using='second')
避免second数据库上相同pk的数据丢失

p=Person(name='Fred')
p.save(using='first')
p.save(using='second',force_insert=True)
保证p在两个数据库中具有相同的主键。如果主键在使用会抛出错误。

选择一个数据库用于删除表单
u=User.objects.using('name').get(username='fred')
u.delete()
u.delete(using='name')

多个数据库上使用管理器
User.objects.db_manager('name').create_user()

自定义查找
from django.db.models import Lookup
class NotEqual(Lookup):
    lookup_name='ne'不能带有'_'
    def as_sql(self,compiler,connection):
        '''
        compiler()返回一个元组，sql字符串和要向字符串插入的参数。
        '''
        lhs,lhs_params=self.process_lhs(compiler,connection)
        rhs,rhs_params=self.process_rhs(compiler,connection)
        params=lhs_params+rhs_params
        (lhs和rhs,Author.objects.filter(name__ne='Jack'),左边是Author模型name字段的引用，右边的值是'Jack')
        使用process_lhs把它们转换为我们需要的SQL值
        return '%s<>%s'%(lhs,rhs),params
    @property
    def output_field(self):
        return FloatField()


from django.db.models.fields import Field
Field.register_lookup(NotEqual)
或使用装饰器
@Field.register_lookup

查询表达式
from django.db.models import F, Count
from django.db.models.functions import Length
Company.objects.filter(num_employees__gt=F('num_chairs'))
F可以做算数运算。
Company.objects.annotate(num_products=Count('products'))
Company.objects.order_by(Length('name').asc()/desc())

内置表达式
F()表达式
reporter=Reporters.objects.get(name='xx')
reporter.stories_filed +=1数值从数据库中取出放到内存中来操作
reporter.save()
使用reporter.stories_filed=F('stories_filed')+1
reporter.save()这是一个描述数据库SQL操作
它就代表了一个指示数据库对该字段进行增量的命令。




数据库函数
Coalesce
接受一个含有至少两个字段名称或表达式的列表，返回第一个非空的值。
参数的类型必须相似。
from django.db.models import Sum.Value as V
from django.db.models.functions import Coalesce
author = Author.objects.annotate(screen_name=Coalesce('','')).get()
print(author.screen_name)

aggregated=Author.objects.aggregate(combined_age=Coalesce(Sum('age'),V(0)))
aggregated['combined_age']

Concat
接受一个含有至少两个文本字段或表达式的列表，返回连接后的文本。
每个参数都必须是文本或者字符类型。使用output_field=CharField()

Length
接受一个文本字段或表达式，返回值的字符个数，表达式是null，长度也是None

Lower还有一个Upper
接受一个文本字符串或表达式，返回它的小写表示形式。

Substr(expression,pos,length=None)
返回字符串pos开始长度是length的子字符串，length如果是None会返回剩余的字段。
Author.objects.annotate(alias=Lower(Substr('name',1,5)))


