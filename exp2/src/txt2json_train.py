import re
import json5

# trainT = open("../dataset/train.txt", 'r')
trainT = open("../dataset/train.txt", 'r')
trainJ = open("../dataset/train.json", 'w')


tryList = [{"text":'asd', 'label':'123'},
    {"text": 'asd', 'label': '123'}]

strPattern = re.compile(r'"(.*)"')

trainList = []
l = 1

for line in trainT:
    if l % 2 == 1:
        # print(line)
        textAndLabel = dict()
        tmp = re.search(strPattern, line).group()
        tmp = re.sub(r'["|\,|\.|\(|\)]',"",tmp)
        textAndLabel['text'] = tmp
    else:
        textAndLabel['label'] = re.match(r"([a-zA-Z]|\-)*", line).group()
        tmpDict = textAndLabel
        trainList.append(tmpDict)
    l += 1



json5.dump(trainList,trainJ, True,indent=2,trailing_commas=False)

trainT.close()
trainJ.close()