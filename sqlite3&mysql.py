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


