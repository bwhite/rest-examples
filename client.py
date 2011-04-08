from restclient import Resource
import random
import json

s = 'http://localhost:8089/'
u0 = str(random.randint(0, 10000))
u1 = str(random.randint(0, 10000))
print (u0, u1)
res = Resource(s)
print res.post('api/%s/' % u0)
print res.post('api/%s/msg' % u0, payload='Immmmm')
msg2_id = json.loads(res.post('api/%s/msg' % u0, payload='sailing'))['msg_id']
print res.post('api/%s/msg' % u0, payload='away')
print res.get('api/%s/' % u0)
print res.delete('api/%s/msg/%s/' % (u0, msg2_id))
print res.post('api/%s/' % u1)
r = res.get()
print(r)
print res.delete('api/%s/' % u0)
r = res.get()
print(r)
