import re
import pandas as pd
from simpletransformers.ner import NERModel, NERArgs
from simpletransformers.classification import ClassificationModel

textPattern = re.compile(r'"(.*)"')
relationClasses = ['Cause-Effect', 'Component-Whole', 'Entity-Destination',
                   'Product-Producer', 'Entity-Origin',
                   'Member-Collection', 'Message-Topic',
                   'Content-Container', 'Instrument-Agency', 'Other']

def readTest(mode=str):
    textList = []
    filename = "test.txt"
    if mode == "dev":
        filename = "dev_"+filename
    else:
        pass
    filename = "../dataset/" + filename
    fp = open(filename, "r")
    for line in fp:
        text = re.search(textPattern, line).group()
        text = re.sub(r'["|\,|\.|\(|\)]', "", text)
        textList.append(text)
    fp.close()
    return textList


modelER = NERModel(
    "roberta", "../models/ner_outputs/", use_cuda=False)

modelClass = ClassificationModel(
    "roberta", "../models/class_outputs/", use_cuda=False)

f = open("../dataset/test.txt", "r")
# 反正不是dev，即直接读取test.txt
textList = readTest("ooo")

tryResult = modelER.predict(["The body of her nephew was in a suitcase under the bed",
                             "The drama unfolded shortly after 7pm last Tuesday (December 22), when Glyn saw that smoke was coming from a bonfire",
                            "Prior to the 4004, engineers built computers either from collections of chips or from discrete components"])

finalResult = modelER.predict(textList)
# print(tryResult[0])
result2file = []
for i in finalResult[0]:
    ans = str()
    entityNum = 0
    indexMax = len(tryResult[0]) - 1
    for index,d in enumerate( i):
        for k in d.keys():
            if d[k] != 'O':
                if entityNum == 0:
                    ans = ans + d[k]
                    ans = ans + '&' + k
                else:
                    ans = ans +',' +k
                entityNum += 1
        if entityNum == 2:
            break
    if entityNum == 0:
        ans = ans + "Other"
        ans = ans + "&" + list(i[-2].keys())[0] + "," + list(i[-1].keys())[0]
    elif entityNum == 1:
        ans = ans + "," + list(i[-1].keys())[0]
    result2file.append(ans)

        

fAns = open("../results/NERResult.txt", "w")
for it in result2file:
    fAns.write(it)
    fAns.write('\n')



