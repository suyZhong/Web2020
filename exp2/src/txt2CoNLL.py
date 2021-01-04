import re
import json5
import pandas as pd
import nltk
import tqdm

NUM = 6400

# trainT = open("../dataset/train.txt", 'r')
num_file = sum([1 for i in open("../dataset/train.txt", "r")])
trainT = open("../dataset/train.txt", 'r')

tryList = [{"text": 'asd', 'label': '123'},
           {"text": 'asd', 'label': '123'}]

strPattern = re.compile(r'"(.*)"')

trainList = []
l = 1
sid = 0
num = 0
tmpList = []

for line in tqdm.tqdm(trainT, total=num_file):
    if l % 2 == 1:
        # print(line)
        text = re.search(strPattern, line).group()
        text = re.sub(r'["|\,|\.|\(|\)]', "", text)
        tmpList = nltk.tokenize.word_tokenize(text)
        listLen = len(tmpList)
    else:
        searchObj = re.search(r"\((.*)\)", line)
        ens = re.sub(r"\(|\)", "", searchObj.group())
        en = ens.split(",",maxsplit=1)
        if ens:
            en1 = en[0]
            en2 = en[1]
        relation = re.match(r"([a-zA-Z\-]*)", line).group()
        for i in tmpList:
            label = str()
            for entity in en:
                entityWord = entity.split(" ")
                if i in entityWord:
                    if entityWord.index(i) == 0:
                        label = "B-" + relation.upper()
                    else:
                        label = "I-" + relation.upper()
                    break
                else:
                    label = "O"
            tmpRow = [sid, i, label]
            trainList.append( tmpRow)
            num += 1
        sid+=1
    l += 1

trainPd = pd.DataFrame(trainList, columns=["sentence_id", "words", "labels"])
trainT.close()

trainPd.to_csv("../dataset/trainNER.csv",index=None,sep="|")
