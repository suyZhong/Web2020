import re
import json5
import pandas as pd
import nltk

NUM = 6400

# trainT = open("../dataset/train.txt", 'r')
trainT = open("../dataset/train.txt", 'r')
trainJ = open("../dataset/trainBaidu.txt", 'w')


tryList = [{"text": 'asd', 'label': '123'},
           {"text": 'asd', 'label': '123'}]

strPattern = re.compile(r'"(.*)"')

trainList = pd.DataFrame( columns=["text","relation"])
l = 1
print(trainList)
for line in trainT:
    if l % 2 == 1:
        # print(line)
        tmpList=[]
        tmp = re.search(strPattern, line).group()
        tmp = re.sub(r'["|\,|\.|\(|\)]', "", tmp)
        tmpList.append(tmp)
    else:
        tmpList.append(re.match(r"([a-zA-Z\-]*)", line).group())
        trainList.loc[int(l/2)] = tmpList
    l += 1

trainT.close()
trainJ.close()
trainList.to_csv("../dataset/trainBaiduCalss.csv",index=None,columns=None,sep="\t")
