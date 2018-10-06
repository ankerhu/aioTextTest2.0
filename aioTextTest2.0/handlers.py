#import re,time,json,logging,hashlib,base64,asyncio
from coroweb import get,post
from models import User,Examination,Title,Question,Mark,Answer,Feedback
from config import configs
from aiohttp import ClientSession
#from gensim.models.doc2vec import Doc2Vec
import sys,json
sys.path.append('../../../')
import calculateTheScore


#testModelD = Doc2Vec.load(r'F:\who\2018firsthalf\myself\这局稳了\coding\corpus\taggedSentences\testModels\doc2vec.model')
appId = configs.mina.appId
appSecret = configs.mina.appSecret
calculate_question_functionDict={
                                '01_zjgk16_mq_01':calculateTheScore.mq_01,
                                '01_zjgk16_mq_02':calculateTheScore.mq_02,
                                '01_zjgk16_mq_03':calculateTheScore.mq_03,
                                '01_zjgk16_mq_04':calculateTheScore.mq_04,
                                '01_zjgk16_mq_05':calculateTheScore.mq_05,
                                '01_zjgk16_yybgyxzgxdwxxsdfz_01':calculateTheScore.yybgyxzgxdwxxsdfz_01,
                                '02_njmn16 _sscsbys_01':calculateTheScore.sscsbys_01,
                                '02_njmn16 _sscsbys_02':calculateTheScore.sscsbys_02,
                                '02_njmn16 _sscsbys_03':calculateTheScore.sscsbys_03,
                                '02_njmn16 _sscsbys_04':calculateTheScore.sscsbys_04,
                                '02_njmn16_krqs_01':calculateTheScore.krqs_01,
                                '02_njmn16_krqs_02':calculateTheScore.krqs_02,
                                '02_njmn16_krqs_03':calculateTheScore.krqs_03
                                }
@get('/')
async def index(**kw):

    #用户登录：接受客户端传来的code和nickname，从微信服务器获取openin和session_key，检索数据库，有则更新，无则增加一条记录
    if kw.get('code',None) and kw.get('nickName',None):
        print(appId)
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
        score = calculate_question_functionDict[kw.get('question_id')](kw.get('answer'))
        answer = Answer(answerText=kw.get('answer'),question_id=kw.get('question_id'),user_id=kw.get('SessionId'),markNumByMachine=score)
        await  answer.save()
        return answer.markNumByMachine
        
    #获取题库以及答案列表
    if kw.get('listName',None):
        examinations = await Examination.findAll()
        for e in examinations:
            e['open'] = False
            e['titles'] = [t for t in await Title.findAll('exam_id=?',e.id)]
            for t in e['titles']:
                t['questions'] = [qs for qs in await Question.findAll('title_id=?',t.id)] 
        return json.dumps(examinations)

    #添加反馈到FeedBack表
    if kw.get('feedback',None) and kw.get('SessionId',None):
        currentUser = await User.find(kw.get('SessionId'))
        feedback = Feedback(feedbackContent=kw.get('feedback'),userId=currentUser.id,nickName=currentUser.nickName)
        await feedback.save()
        return 'done'

    #根据titleId查询user，并返回respondents
    if kw.get('titleId',None):
        respondents = {}
        for question in await Question.findAll('title_id=?',kw.get('titleId')):
            for answer in await Answer.findAll('question_id=?',question.id,orderBy='create_at asc'):
                u = await User.find(answer.user_id)
                pickerArray = ['请选择分数，确定即提交',0]
                for i in range(question.fullMark):
                    pickerArray.append(i+1)
                if answer.user_id + u.nickName in respondents:
                    #用user_id加上nickName作为key是避免出现用户有相同昵称，所以在value中还加上了user_id，方便客户端将key中的user_id去掉
                    respondents[answer.user_id + u.nickName].append({'user_id':answer.user_id,'answer_id':answer.id,'answerText':answer.answerText,'markNumByMachine':answer.markNumByMachine,'question_id':answer.question_id,'pickerArray':pickerArray,'pickerIndex':0,'display':'none'})
                else:
                    respondents[answer.user_id + u.nickName]=[{'user_id':answer.user_id,'answer_id':answer.id,'answerText':answer.answerText,'markNumByMachine':answer.markNumByMachine,'question_id':answer.question_id,'pickerArray':pickerArray,'pickerIndex':0,'display':'none'}]
        return json.dumps(respondents)

    
    #根据titleId查询对应用户的答案
    if kw.get('answeredTitleId',None):
        questionsAnswered=[]
        for question in await Question.findAll('title_id=?',kw.get('answeredTitleId')):
            questionsAnswered.append({'questionContent':question.questionContent,'markReference':question.markReference,'id':question.id,'answers':[]})
        return json.dumps(questionsAnswered)

    #获取用户评分，存到Mark表中
    if kw.get('markNumByUser',None) and kw.get('user_mark_id',None) and kw.get('answer_id',None):
        mark = Mark(user_mark_id=kw.get('user_mark_id'),answer_id= kw.get('answer_id'),markNumByUser=kw.get('markNumByUser'))
        await mark.save()
        return '稳了'

    #根据I_mark_sessionId和questions数组得到I_mark_table表格
    if kw.get('I_mark_sessionId',None) and kw.get('questionIds',None):
        I_mark_table = {}
        for marksByMe in await Mark.findAll('user_mark_id=?',kw.get('I_mark_sessionId'),orderBy='create_at asc'):#查询该用户打得分，按时间升序排列
            for questionId in json.loads(kw.get('questionIds')):
                I_mark_table.setdefault(questionId,[])
                for answer in await Answer.findAll('question_id=?',questionId,orderBy='create_at asc'):#查询某道题的回答，按时间升序排列
                    #当该用户打分的answer_id与根据question_id查询到的answer_id相等时，则是该用户给这道题打的所有分，有可能同道题同个人答了多次，也可能给同个人的一次答题打了多次分
                    if answer.id == marksByMe.answer_id:
                        userAnswered = await User.find(answer.user_id)
                        I_mark_table[questionId].append({'answerText':answer.answerText,'userNickname':userAnswered.nickName , 'markNumByMachine':answer.markNumByMachine , 'markNumByUser':marksByMe.markNumByUser})
        return json.dumps(I_mark_table)

    #根据sessionId和questions数组得到I_mark_table表格
    if kw.get('mark_me_sessionId',None) and kw.get('questionIds',None):
        mark_me_table={}
        for questionId in json.loads(kw.get('questionIds')):
            mark_me_table.setdefault(questionId,[])
            for answer in await Answer.findAll('question_id=?',questionId,orderBy='create_at asc'):
                if answer.user_id == kw.get('mark_me_sessionId'):
                    tableList = []
                    for mark in await Mark.findAll('answer_id=?',answer.id):
                        user = await User.find(mark.user_mark_id)
                        tableList.append({'userNickname':user.nickName,'markNumByUser':mark.markNumByUser})
                    mark_me_table[questionId].append({'answerText':answer.answerText,'markNumByMachine':answer.markNumByMachine,'table':tableList})                    
        return json.dumps(mark_me_table)
            
@get('/test')
async def test(**kw):
    return {
        '__template__': 'test.html'
    }