import requests
p={'tel':1,'personId':'001','agreement':True,'id':41}
p2={'house':5792,'id':41,'value':11}
i=0
p3={'id':41}
cookie=dict(sessionid='09doixacqg2m1a0rayyas4awccp5t4iu')
cookie2=dict(token='ea566ddec685abf0a2caeb79d5883831',random='79421')
for i in range(0,30):
	#requests.post(" http://10.7.1.34:5050/app/orderconfirm/",data=p2,cookies=cookie)
	#requests.get("http://10.7.1.34:5050/app/detail/",data=p3,cookies=cookie)
	#requests.get("http://10.7.1.34:5050/static/m/views/choiceHouse.html?id=41")
	#requests.get("http://10.7.1.34:5050/acc/cuslog/?tel=1&personId=001&agreement=true&id=41")
	r=requests.post("http://10.7.1.34:5050/acc/cuslog/",data=p,cookies=cookie2)
