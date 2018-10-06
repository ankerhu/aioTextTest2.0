import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.doc2vec import Doc2Vec
import sys,re
sys.path.append('../../../')
from preprocessTheTxt import cut_sentence

testModelD = Doc2Vec.load(r'F:\who\2018firsthalf\myself\这局稳了\coding\corpus\taggedSentences\testModels\doc2vec.model')
'''
暂时用不上
#对列表进行全排列
def permutation(myList):
    if len(myList) > 1:
        myLists = []
        tempList = myList[:]
        tempList.remove(myList[0])
        for l in permutation(tempList):
            #注意循环次数要加一，不然插入不到最后一个位置
            for index in range(len(l) + 1):
                #注意l要保护起来
                tempL = l[:]
                tempL.insert(index,myList[0])
                myLists.append(tempL)
        return myLists
    else:  
        return [myList]
'''


'''
该算法为最大分数匹配算法，但发现并不适用，因为现实打分是找点给分，有可能并不合适的点分数之和比只踩对某个点要多，导致分数不准确的情况


#计算答案的所有词语与参考词语的相似度，挑选出最大的，以尽量多给分为原则
def calculateWordSimilarity(answer, *allReferencesGroups):
    answerWords = cut_sentence(answer)[0].split()
    #组合的循环，每种组合都算一遍，取组合中几项相加和最大的为最终结果
    for referencesGroup in allReferencesGroups[0]:
        similarityList = []
        maxSumSimilarityList = 0
        #注意保护原answerWords，因为每次更换组合会对列表进行remove操作
        tempAnswerWords = answerWords[:]
        #某组合中所有参考词列表循环
        for references in referencesGroup:
            maxSimilarity = 0.0
            maxW = 0
            #列表内可选关键词循环
            for r in references:
                for w in tempAnswerWords:
                    wrSimilarity = testModelD.similarity(w,r)
                    if wrSimilarity >= maxSimilarity:
                        maxSimilarity = wrSimilarity
                        maxW = w
            #把与第一个参考词相似度最大的答案词全部移出tempAnswerWords
            for i in range(tempAnswerWords.count(maxW)):
                tempAnswerWords.remove(maxW)
                print(maxW)
            similarityList.append(maxSimilarity)
            sumSimilarityList = sum(similarityList)
            if sumSimilarityList >= maxSumSimilarityList:
                maxSumSimilarityList = sumSimilarityList
                result = similarityList
    return result
'''

#找点给分，根据答案点进行循环，所有回答词与所有答案点进行匹配，找到最大的，然后记录下来并remove掉该回答词和答案点，直到答案点都遍历完，注意不是从第一个答案点开始遍历，而且遍历所有答案点
def calculateWordSimilarity(answer, *referenceWordsList):
    answerWords = cut_sentence(answer)[0].split()
    similarityList=[]
    while len(referenceWordsList[0]) >0:
        maxSimilarity=0.0
        maxWord = ''
        maxRefereceWordsIndex = 0
        if len(answerWords) > 0:
            index = 0
            #不同答案点循环
            for referenceWords in referenceWordsList[0]:
                #答案点中关键词循环
                for referenceWord in referenceWords:
                        #回答词循环
                        for answerWord in answerWords:
                            try:
                                wrSimilarity = testModelD.similarity(answerWord,referenceWord)
                            except KeyError as e:
                                print(e)
                                wrSimilarity = 0.0
                            if wrSimilarity >= maxSimilarity:
                                maxSimilarity = wrSimilarity
                                maxWord = answerWord
                                maxRefereceWordsIndex = index
                                '''
                                print(maxSimilarity)
                                print(maxWord)
                                print(referenceWord)
                                '''
                index += 1
        else:#说明回答词还没答案点多,立刻停止循环
            break 
        #移除回答词这次循环中所有最相似的词
        for i in range(answerWords.count(maxWord)):
            answerWords.remove(maxWord)
        referenceWordsList[0].pop(maxRefereceWordsIndex)
        similarityList.append(maxSimilarity)
    return similarityList



def calculateSentenceSimilarity(answer,*referenceSentencesList):
    answerSentences = re.split(r'[。？！，；\n…]+[。？！，；\n…]*',answer)
    answerSentenceCuts = [cut_sentence(answerSentence)[0].split() for answerSentence in answerSentences if answerSentence != '']
    similarityList = []
    while len(referenceSentencesList[0]) >0:
        minDistance = 100
        minAnswerSentenceCut = []
        minReferenceSentenceIndex = 0
        if len(answerSentenceCuts) > 0:
            index = 0
            #答案点循环
            for referenceSentences in referenceSentencesList[0]:
                #答案点中关键句循环
                for referenceSentence in referenceSentences:
                    referenceSentenceCut = cut_sentence(referenceSentence)[0].split()
                    #回答句循环
                    for answerSentenceCut in answerSentenceCuts:
                        distance = testModelD.wmdistance(referenceSentenceCut,answerSentenceCut)
                        if distance <= minDistance:
                            minDistance = distance
                            minAnswerSentenceCut = answerSentenceCut
                            minReferenceSentenceIndex = index
                            
                            print(distance)
                            print(minAnswerSentenceCut)
                            print(referenceSentenceCut)
                            
                index += 1
        else:#说明回答句还没答案点多,立刻停止循环
            break
        #移除回答句里这里循环中所有最相似的句子
        for i in range(answerSentenceCuts.count(minAnswerSentenceCut)):
            answerSentenceCuts.remove(minAnswerSentenceCut)
        referenceSentencesList[0].pop(minReferenceSentenceIndex)
        similarityList.append(minDistance)
    return similarityList


def mq_01(answer):
    referenceWords1=['忙碌','繁忙']
    referenceWords2=['辛苦','辛勤','辛劳','劳累','繁重','琐碎','费力','起早贪黑','艰苦','繁琐','任劳任怨','艰辛','劳苦']
    referenceWordsList = [referenceWords1,referenceWords2]
    score = 0
    for similarity in calculateWordSimilarity(answer,referenceWordsList):
        print(similarity)
        if similarity >= 0.27:#0.27来自“疲惫”的相似度
            score += 1
        
    return score


def mq_02(answer):
    referenceSentences1=['透露了母亲内心的急迫','表现出母亲的急躁','透露了母亲内心焦躁','透露了母亲的紧迫之感','渲染一种急迫、忙碌的气氛']
    referenceSentences2=['表现了母亲劳作的忙碌','表现了母亲勤劳忙碌','表现了母亲从不停歇','表现了母亲很少休息','表现了母亲繁忙','表现了母亲辛劳','表现了母亲劳碌','表现了母亲忙于家中的活儿']
    referenceSentences3=['反映了母亲对家庭的责任感','反映了母亲对家庭的责任心','反映了母亲为家庭无私付出','反映了母亲辛劳持家，甘于劳累','反映了家庭生活离不开母亲','反映了母亲忙于家中琐事','反映了母亲被家庭束缚失去自由的艰辛无奈']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        if distance < 7.73:#8.5来自于“透露了母亲的责任心”的距离
            score += 1
    return score
    
def mq_03(answer):
    referenceSentences1=['在结构上起贯穿全文的作用','贯穿其中，使文章更连贯','起到承接与转折的作用']
    referenceSentences2=['母亲向往又犹疑的复杂心理','母亲的矛盾心理','母亲想看火车但无法实现的愿望','母亲对火车好奇，但又对生活顺从和无力反抗','母亲想去却不能去','母亲看火车的犹疑与胆怯','母亲虽然想去但仍选择不去','母亲想去却仍不勇于抽出时间去看火车','母亲一次次想看但一次次无法去看火车','反映了母亲的优柔寡断']
    referenceSentences3=['询问的不厌其烦与回答的不胜其烦形成对照，丰富了母亲的形象','形成反衬','形成对比','形成对照']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    #print(calculateSentenceSimilarity(answer,referenceSentencesList))
    #在calculateSentenceSimilarity函数中会对referenceSentencesList做出修改，所以在真正算分之前不要调用calculateSentenceSimilarity函数
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 7.5:#7.5来自于“询问和回答形成了对比”的距离
            score += 1
    return score

def mq_04(answer):
    referenceSentences1=['通过比喻、排比','通过比喻']
    referenceSentences2=['渲染了火车的神奇与母亲对火车的痴迷','火车的神奇','母亲对火车的痴迷','火车是像蛇一样的怪物','母亲对火车的幻想','母亲对火车的向往']
    referenceSentences3=['通过神态、动作等细节，细腻描写','幻想、闭上眼睛、失神等神态，放下、抛开、烧焦等动作']
    referenceSentences4=['母亲好奇、陶醉和渴望的心理','对火车与远方的向往','对火车的极大兴趣']
    referenceSentences5=['叙事上有过渡、舒缓节奏等作用','引出下文']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3,referenceSentences4,referenceSentences5]
    score = 0
    #print(calculateSentenceSimilarity(answer,referenceSentencesList))
    #在calculateSentenceSimilarity函数中会对referenceSentencesList做出修改，所以在真正算分之前不要调用calculateSentenceSimilarity函数
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 6.3:#7.5来自于“表现母亲对火车的讨厌”的距离
            score += 1
    #5点，答对4点给满分
    if score > 4:
        score = 4
    return score

def mq_05(answer):
    referenceSentences1=['母亲是朴实、坚忍、勤勉持家的传统女性','母亲是朴实、坚忍、勤勉持家的农村妇女','母亲是朴实、坚忍、勤勉持家的山村妇女']
    referenceSentences2=['母亲受到新事物的感召','具有尝试新生活的内在倾向']
    referenceSentences3=['母亲受传统和现实的羁绊','缺乏将希望变为行动的自觉和勇气']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    #print(calculateSentenceSimilarity(answer,referenceSentencesList))
    #在calculateSentenceSimilarity函数中会对referenceSentencesList做出修改，所以在真正算分之前不要调用calculateSentenceSimilarity函数
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 10:#9.6来自于“母亲是个朴实无华的农村女性”的距离
            score += 2
    return score

def yybgyxzgxdwxxsdfz_01(answer):
    referenceSentences1=['有益于白话语言的艺术化','艺术化']
    referenceSentences2=['丰富了现代文学创作的表现形式','现代创作吸收了文言因素和成分','文言融入现代文学创作实践中','促进了中国现代文学形式的发展','为现代作家提供了深厚的文化内涵和底蕴']
    referenceSentences3=['参与了语言变迁与中国现代文学形式演进的过程']
    referenceSentencesList1 = [referenceSentences1,referenceSentences2]
    referenceSentencesList2= [referenceSentences3]
    score = 0
    #答案点1和2分别为两分
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList1):
        #print(distance)
        if distance < 6:#6来自于“现代文学”的距离
            score += 2
    #答案点3得一分
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList2):
        #print(distance)
        if distance < 9.5:#9.5来自于“文言也加入到现代创作中”的距离
            score += 1
    if score > 3:
        score = 3
    return score

def sscsbys_01(answer):
    referenceSentences1=['突出北方冬天的强悍和漫长']
    referenceSentences2=['为下文写人们渴盼春天作铺垫']
    referenceSentencesList = [referenceSentences1,referenceSentences2]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 8:#8来自于“铺垫出人们对春天的渴望”的距离，该题答案参考少，所以范围较大
            score += 2
    return score    

def sscsbys_02(answer):
    referenceSentences1=['序幕拉得很长']
    referenceSentences2=['万物蓄势待发','万事万物蓄势待发']
    referenceSentences3=['春色亮相时热烈迅猛']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 10:#10来自于“拉长了序幕，万事万物蓄势待发，春色亮相时突出了热烈”
            score += 2
    return score

def sscsbys_03(answer):
    referenceSentences1=['对岁月流逝的感叹','对岁月流逝的感慨']
    referenceSentences2=['对爱人深切而真挚的怀念']
    referenceSentencesList = [referenceSentences1,referenceSentences2]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 8.5:#8.5来自于“感慨时间的流逝，怀念爱人”
            score += 2
    return score 

def sscsbys_04(answer):
    referenceSentences1=['用反问句式，强烈表达作者对春色的独特感受']
    referenceSentences2=['以景（“春色”）与情（“忧伤”）的强烈反差，激发读者的阅读兴趣']
    referenceSentences3=['统摄全篇思路，由寻常春色写到忧伤春色','统领全文的写作思路']
    referenceSentences4=['奠定全文忧伤的感情基调']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3,referenceSentences4]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 6:#6来自于乱答
            score += 2
    if score > 6:
        score = 6
    return score     

def krqs_01(answer):
    referenceSentences1=['能说会写，左右视听','能说会道，混淆视听','能说会写,混淆视听','能说会道,左右视听']
    referenceSentences2=['主张宽容，鼓吹均衡']
    referenceSentences3=['居高临下，脱离现实']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
       # print(distance)
        if distance < 10:#12来自于“能说会道，主张宽容，脱离现实”
            score += 2
    return score

def krqs_02(answer):
    referenceSentences1=['先亮出对方的观点']
    referenceSentences2=['再指出其恶劣的手段']
    referenceSentences3=['接着揭示其荒谬后果']
    referenceSentences4=['最后指出其自相矛盾之处']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3,referenceSentences4]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 9:#9来自于上一道题，“能说会道，主张宽容，脱离现实”
            score += 2
    return score    

def krqs_03(answer):
    referenceSentences1=['宽容论认为万物无是非，但人们凭常识经验和理性可以定出是非标准']
    referenceSentences2=['宽容论貌似宽容一切，但对触犯他们的言谈并不宽容']
    referenceSentences3=['宽容论把一切托付给市场经济，否定人的能动作用']
    referenceSentencesList = [referenceSentences1,referenceSentences2,referenceSentences3]
    score = 0
    for distance in calculateSentenceSimilarity(answer,referenceSentencesList):
        #print(distance)
        if distance < 8:#8来自于上一道题，“能说会道，主张宽容，脱离现实”
            score += 2
    return score

#print(sscsbys_04('测试'))