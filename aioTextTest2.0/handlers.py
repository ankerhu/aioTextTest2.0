import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer

@get('/')
async def index(*,code='',cc=''):
    #users = await User.findAll()
    answer=''
    if code == '123':
        answer = '迷人的反派角色'
        return answer
    if cc:
        return cc


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='create_at desc')
    for u in users:
        u.feedback = '*****'
    return dict(users=users)