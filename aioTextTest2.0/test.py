import orm,asyncio
from models import User
async def test():
	await orm.create_pool(loop,user='root',password='196392zwx',db='texttest')
	u = User(openid='test openid',sessionId = 'test sessionId',feedback='test feedback')
	await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()
print('done')