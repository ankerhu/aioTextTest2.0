import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer
from config import configs
from aiohttp import ClientSession
import json

appId = configs.mina.appId
appSecret = configs.mina.appSecret

@get('/')
async def index(**kw):
    #用户登录：接受客户端传来的code和nickname，从微信服务器获取openin和session_key，检索数据库，有则更新，无则增加一条记录
    if kw.get('code',None) and kw.get('nickName',None):
        wxAPIURL = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appId,appSecret,kw['code'])
        async with ClientSession() as session:
            async with session.get(wxAPIURL) as resp:
                #resp.text()是json格式的文本，需处理
                openidAndsession_key =  json.loads(await resp.text())
        u = await User.findAll('openid=?',[openidAndsession_key.get('openid')])
        if u:
            return u[0].get('openid') + u[0].get('nickName')
        else:
            u = User(openid = openidAndsession_key.get('openid'),session_key=openidAndsession_key.get('session_key'),nickName=kw['nickName'])
            await u.save()
            return kw['nickName']
    if kw.get('openid',None):
        return kw['openid']
