import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.doc2vec import Doc2Vec
import sys
sys.path.append('../../../')
from preprocessTheTxt import cut_sentence

testModelD = Doc2Vec.load(r'F:\who\2018firsthalf\myself\这局稳了\coding\corpus\taggedSentences\testModels\doc2vec.model')
print('keyi')