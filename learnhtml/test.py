import requests
p={'tel':1,'personId':'001','agreement':True,'id':41}
p2={'house':5787,'id':41,'value':24}
i=0
for i in range(0,15):
	requests.post(" http://10.7.1.34/app/orderconfirm/",data=p2)
	
    
    
