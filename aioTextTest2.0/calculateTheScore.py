import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.doc2vec import Doc2Vec
import sys
sys.path.append('../../../')
from preprocessTheTxt import cut_sentence

testModelD = Doc2Vec.load(r'F:\who\2018firsthalf\myself\这局稳了\coding\corpus\taggedSentences\testModels\doc2vec.model')

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
            for referenceWords in referenceWordsList[0]:
                for referenceWord in referenceWords:
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
                                print(maxSimilarity)
                                print(maxWord)
                                print(referenceWord)
                index += 1
        else:#说明回答词还没答案点多,立刻停止循环
            break 
        for i in range(answerWords.count(maxWord)):
            answerWords.remove(maxWord)
            referenceWordsList[0].pop(maxRefereceWordsIndex)
            similarityList.append(maxSimilarity)
    return similarityList

def mq_01(answer):
    referenceWords1=['忙碌','繁忙']
    referenceWords2=['辛苦','辛勤','辛劳','劳累','繁重','琐碎','费力','起早贪黑','艰苦','繁琐','任劳任怨','艰辛']
    referenceWordsList = [referenceWords1,referenceWords2]
    score = 0
    for similarity in calculateWordSimilarity(answer,referenceWordsList):
        if similarity >= 0.234:#0.234来自“累”与referenceWords2的相似度
            score += 1
        print(similarity)
    return score
print(mq_01(u'表现了母亲开心和风尘仆仆'))