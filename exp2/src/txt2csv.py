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

trainList = pd.DataFrame( columns=["text","relation","entity1","entity2"])
l = 1
print(trainList)
for line in trainT:
    if l % 2 == 1:
        # print(line)
        tmpList=[]
        textAndLabel = dict()
        tmp = re.search(strPattern, line).group()
        tmp = re.sub(r'["|\,|\.|\(|\)]', "", tmp)
        tmpList.append(tmp)
    else:
        tmpList.append(re.match(r"([a-zA-Z\-]*)", line).group())
        searchObj = re.search(r"\((.*)\)", line)
        ens = re.sub(r"\(|\)", "", searchObj.group())
        en = ens.split(",",maxsplit=1)
        if ens:
            en1 = en[0]
            en2 = en[1]
        tmpList.append(en1)
        tmpList.append(en2)
        trainList.loc[int(l/2)] = tmpList
    l += 1

trainT.close()
trainJ.close()
trainList.to_csv("../dataset/train.csv",index=None)
