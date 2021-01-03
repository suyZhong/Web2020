import numpy as np
import pandas as pd
import gensim
import re
from gensim.models.doc2vec import Doc2Vec,LabeledSentence,TaggedLineDocument
import tqdm


def labelizeReviews(reviews, label_type):
    labelized = []
    for i, v in enumerate(reviews):
        label = '%s_%s' % (label_type, i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized

size = 4000
epochNum = 10

trainData = []
testData = []
f = open("../dataset/trainBaiduCalss.txt", 'r')
for l in f:
    trainData.append(l.split()[0])
f.close()

f = open("../dataset/testpure.txt", 'r')
for l in f:
    testData.append(re.sub("\n", "", l))
f.close()

print(trainData[:5])
print(testData[:5])

trainData = labelizeReviews(trainData, 'TRAIN')
testData = labelizeReviews(testData, 'TEST')

Data = trainData + testData

model_dm = gensim.models.Doc2Vec(
    min_count=1, window=10,vector_size=size, sample=1e-3, negative=5, workers=3,epochs=10)
#使用所有的数据建立词典
model_dm.build_vocab(trainData + testData)

model_dm.train(Data,total_examples=model_dm.corpus_count,epochs=model_dm.epochs)

#训练测试数据集

model_dm.save("../models/model.d2v")


