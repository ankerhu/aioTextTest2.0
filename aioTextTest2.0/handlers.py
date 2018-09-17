import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer
from config import configs
from aiohttp import ClientSession
import json
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.doc2vec import Doc2Vec
import sys
sys.path.append('../../../')
from preprocessTheTxt import cut_sentence

testModelD = Doc2Vec.load(r'F:\who\2018firsthalf\myself\这局稳了\coding\corpus\taggedSentences\testModels\doc2vec.model')
appId = configs.mina.appId
appSecret = configs.mina.appSecret

@get('/')
async def index(**kw):

    #用户登录：接受客户端传来的code和nickname，从微信服务器获取openin和session_key，检索数据库，有则更新，无则增加一条记录
    if kw.get('code',None) and kw.get('nickName',None):
        wxAPIURL = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appId,appSecret,kw.get('code'))
        async with ClientSession() as session:
            async with session.get(wxAPIURL) as resp:
                #resp.text()是json格式的文本，需处理
                openidAndsession_key =  json.loads(await resp.text())
        currentUser = await User.find(openidAndsession_key.get('openid'))
        if currentUser:
            #以防用户改过微信昵称，每次登录及时储存当前微信昵称
            currentUser.nickName = kw.get('nickName')
            await currentUser.update()
            #返回openid字符串作为SessionId
            return currentUser.id
        else:
            #openid字符串同时作为主键便于查找
            currentUser = User(id = openidAndsession_key.get('openid'),session_key=openidAndsession_key.get('session_key'),nickName=kw.get('nickName'))
            await currentUser.save()
            return currentUser.id

    #获取用户答案，更新Answer表
    if kw.get('answer',None) and kw.get('question_id',None) and kw.get('SessionId',None):
        
        answer = Answer(answerText=kw.get('answer'),question_id=kw.get('question_id'),user_id=kw.get('SessionId'))
        await  answer.save()
        return answer.id
        
    #获取题库以及答案列表
    if kw.get('listName',None):
        examinations = await Examination.findAll()
        for e in examinations:
            e['open'] = False
            e['titles'] = [t for t in await Title.findAll('exam_id=?',e.id)]
            for t in e['titles']:
                t['questions'] = [qs for qs in await Question.findAll('title_id=?',t.id)] 
        return json.dumps(examinations)