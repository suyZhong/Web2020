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

trainList = pd.DataFrame( columns=["文本内容","实体关系1"])
l = 1
print(trainList)
for line in trainT:
    if l % 2 == 1:
        # print(line)
        tmpList=[]
        text = re.search(strPattern, line).group()
        text = re.sub(r'["|\,|\.|\(|\)]', "", text)
        tmpList.append(text)
    else:
        searchObj = re.search(r"\((.*)\)", line)
        ens = re.sub(r"\(|\)", "", searchObj.group())
        en = ens.split(",",maxsplit=1)
        if ens:
            en1 = en[0]
            en2 = en[1]
        en1tag = nltk.pos_tag(en1)[1][1]
        en2tag = nltk.pos_tag(en2)[1][1]
        en1Pos = re.search(en1, text).span()
        en2Pos = re.search(en2, text).span()
        entity1 = "{[" + str(en1Pos[0]) + "," + str(en1Pos[1])+"]," + en1tag+"}"
        entity2 = "{[" + str(en2Pos[0]) + "," + str(en2Pos[1]) + "]," + en2tag + "}"
        rAe = entity1+","+entity2+","+re.match(r"([a-zA-Z\-]*)", line).group()
        tmpList.append(rAe)
        trainList.loc[int(l/2)] = tmpList
    l += 1

trainT.close()
trainJ.close()
trainList.to_csv("../dataset/trainBaidu.csv",index=None,sep="|")
