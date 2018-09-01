import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer
from config import configs
from aiohttp import ClientSession

appId = configs.mina.appId
appSecret = configs.mina.appSecret

@get('/')
async def index(**kw):
    if kw.get('code',None):
        wxAPIURL = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appId,appSecret,kw['code'])
        async with ClientSession() as session:
            async with session.get(wxAPIURL) as resp:
                return await resp.text()
    if kw.get('session_key',None):
        return kw['session_key']
