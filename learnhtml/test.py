import requests
p={'tel':1,'personId':'001','agreement':True,'id':41}
p2={'house':5787,'id':41,'value':11}
i=0
p3={'id':41}
cookie=dict(sessionid='96rmn1wlkor8nqhf2iins4r3kd355f1k')
for i in range(0,12):
	#requests.post(" http://10.7.1.34/app/orderconfirm/",data=p3,cookies=cookie)
	#requests.get("http://10.7.1.34/app/detail/?id=41")
	requests.get("http://10.7.1.34:5050/static/m/views/choiceHouse.html?id=41")
