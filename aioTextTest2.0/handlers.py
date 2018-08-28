import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer

@get('/')
async def index(request):
    users = await User.findAll()
    return{
        '__template__' : 'test.html',
        'users' : users
    }