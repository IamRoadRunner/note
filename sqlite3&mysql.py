from sqlite3 import connect
:memory:内存里存储
con=sqlite3.connect('name.db')
cur=con.cursor()
/////////////////////////////////
from mysql.connector import connect
db_name={
	"host":"localhost",
	"port":3306,
	"user":"root",
	"password":""
	"database":"name.db"
}
con=connect(**db_name)
cur=con.cursor()
row=(1,2,3)
//////////////////////////////////



cur.execute('select,update,delete,insert into')
cur.execute('updata tb_name(column) values(?,?)',(one,two))


rows=[(),(),()]#批量插入的数据
cur.executemany('insert into tb_name(columns) values(?,?,?)',rows)


cur.fetchone()
cur.fetchmany(size) arraysize=size
cru.fetchall()


con.close()


from sqlite3 import Row
con.row_factory=Row
#引入行对象
row=cur.fetchone()
print('',row['columnname'])
for item in row:
	print(item)#以列为元素迭代


for row in cur:
	for r in row:
		print(i)#每一行的每一列


sql_str="""
create table
insert into
........
"""
cur.executescript(sql_str)


def check(arg):
	pass
con.create_function('checkn',1,check)
			#函数注册后的名，1个参数，要注册的函数
cur.execute('select id,checkn(arg) form tb_name')


class a:
	def b:
	def c:
con.create_aggregate('an',1,a)
cur.execute('select id,b(arg) form tb_name')

con.commit()!!!!!!!!!!!!!!!!!!!!!!!


sql语句
select distinct columnname from tablename where 
and/or order by xx desc/asc. 

insert into tablename values ()
insert into tablename(columnname) values ()

update tablename set a=x where xxx

delete from talbename where xxx删除一行
delete from tablename 删除表中的所有行
或delete * from tablename

top子句
select top # */top # percent from tablename
select * from tablename limit #

like操作符
like pattern 
like 'n%'以n开头
like '%y'以y结尾
like '%l%'包含l
not like 不包含
% 代替一个或多个字符
_ 代替一个字符
[charlist]列中任意一个
[^charlist]不在列中任意一个[!charlist]
[charlist]%

in操作符
select * from tablename where com in ('x','y')

between操作符
取数据范围之内的
where com between 'a' and 'b'
          not between 

alias别名
select po.order,p.name from person as p,product as po where p.age=21 and po.id=3
select lastname as name from person#结果是别名的

join引用两个表中的数据
select p.name,o.orderno from person as p,orders as o where p.id_p = o.id_p
select p.name,o.orderno from person as p inner join orders as o on p.id_p = o.id_p
left join 不管有没有匹配返回左表的所有/right join
full join 左右的都返回

union和union all操作符
合并两个或多个查询语句结果集，
select ... union select ...相同数量的列，相似的数据类型，列的顺序必须相同。
union all允许重复的值。

select into 从一个表中选取数据，然后把数据插入另一个表/创建表的备份复件
select */com into newtablename from tablename

创建数据库语句
create database dataname
create table(
com1 type,
com2 type,
)

约束
not null 不接受NULL值
unique唯一标识
	unique约束唯一标识数据库中的每条记录
	create table my(
	id_p int NOT NULL UNIQUE,#可以直接加
	name varchar(255),
	age int,
	where varchar(255),
	unique（name）#可以后边声明，取决于不同的数据库
	constraint uc_p unique(age, where)|使用于primary key
	)
	如果表被创建了要增加约束
	alter table tbname add unique(com)
	alter table tbname add constraint uc_p unique(com1,com2)
	撤销约束
	alter table tbname drop constraint uc_p   

primary key约束
	主键必须包含唯一值，不能包含null，每个表都有一个主键
	create table my(
	id_p int NOT NULL UNIQUE PRIMARY KEY#可以这里声明,
	PRIMARY KEY(id_p)#可以这里声明
	)

foreign key约束

	person（id_p,name,city）
	order(id_o,orderno,id_p)
	create table person(
	id_p int not null,
	name varchar(255),
	city varchar(255),
	primary key(id_p)
	)

	create table order(
	id_o int not null,
	orderno int,
	id_p int,#id_p int foreign key references person(id_p)
	primary key(id_o),
	foreign key(id_p) references person(id_p)
	)
	create table order(
		id int not null,
		name varchar(255),
		p_id int not null,
		primary key(id),
		foreign key(p_id) references person(id_p)
		)

	外键要求：
	order中id_p不能是主键；
	person中的id_p须是主键；
	两个字段数据类型需要是相同的。

	alter table tbname add foreign key(id_p) references person(id_p)
	alter table tbname add constraint uc_p foreign key(id_p) references person(id_p)

	alter table tbname drop foreign key name;
			    drop constraint name;


check约束
用于限制列中的值的范围
create table person(
	id_p int not null,#id_p int not null primary key check(id_p>0)
	name varchar(255),
	city varchar(255),
	primary key(id_p),
	check（id_p>0）
	constraint ch_na check(name='x' and city = 'y')
	)


	alter table tbname add check()
	alter table tbname add constraint uc_p check()

	alter table tbname drop check name;
			    drop constraint name;

default 约束
插入默认值
alter table tbname alter city set defautl 'xx'
	           alter column city set default 'xx'

		   alter city drop default/alter column city drop default 

create index 创建索引
	表中创建索引，快速高效的查询数据。
	create (unique)index index_name on tbname(column_name DESC(columns))

drop 语句
	drop index index_name on tbname
	drop index tbname.index_name
	alter table tbname drop index index_name

	drop table tbname
	drop database dbname

	truncate table tbname清除表内的数据
alter table在已有的表中添加，修改或删除列
	alter table tbname add column_name type ;
	alter table tbname drop column_name;
	alter table tbname alter column_name type;
auto increment在新纪录插入表中时生成一个唯一的数字
create table person(
	id_p int not null auto_increment/identity(20起,10步长),#起始值是1，递增1
	name varchar(255),
	city varchar(255),
	primary key(id_p)
	)

sql view
create view [view_name] as select column_name(s) from tbname where xxx
select * from [view_name]

date
date,datetime,timestamp,year.

NULL
IS NULL /IS NOT NULL

ISNULL(column,0)
NVL(column,0)
IFNULL(column,0)

內建函数
select function(column) from tbname
合计函数
	avg()
		select customer from orders where o>(select avg(o) from order)
	count()返回匹配指定条件的行数。NULL不计入
		count(distinct column_name) 不重复的
		count(*)总行数
		first()指定字段中第一个记录的值
		last()
		max()返回一列中最大的
		min()返回最小的
		sum()一列总和
	group by()
		select customer ,sum(price) from order group by customer#按每个customer分组求price和
	having()
		select customer,sum(orderprice) from order group by customer having sum(orderprice)<2000
scalar函数(标量函数)
	ucase()把字段值转换成大写
	lcase()小写
	mid()截取 mid(column start1, length)
	len()返回字段值的长度
	round(column,2)四舍五入指定小数位数
	now()返回时间
	format(column, format),format(now(),'yyyy-mm-dd')

grant all privileges on *.* to root@...  identified by '1' with grant option;
flush privileges;
























