import orm,asyncio
from models import User
async def test():
	await orm.create_pool(loop,user='root',password='196392zwx',db='texttest')
	u = User(openid='test openid',sessionId = 'test sessionId',feedback='test feedback')
	await u.save()
async def testFind():
	await orm.create_pool(loop,user='root',password='196392zwx',db='texttest')
	u = await User.find('0015354744517956edac730a0d14873aba5f4ece018a8c2000')
	u.openid = '9090'
	r = await  u.update()
	print(r)

loop = asyncio.get_event_loop()
loop.run_until_complete(testFind())
loop.close()
print('done')