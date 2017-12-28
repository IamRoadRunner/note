import requests
p={'tel':1,'personId':'001','agreement':True,'id':41}
p2={'house':5787,'id':41,'value':11}
i=0
p3={'id':41}
cookie=dict(cookies_sessionid='77xblj6ebwbn55qqcot97usp3e8h7886')
for i in range(0,150):
	#requests.post(" http://10.7.1.34/app/orderconfirm/",data=p3,cookies=cookie)
	requests.get("http://10.7.1.34/app/eventinfo/?id=41")
    
    
