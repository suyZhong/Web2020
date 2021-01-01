import re
import json5

testT = open("../dataset/test.txt", 'r')
testJ = open("../dataset/test.json", 'w')


tryList = [{"text":'asd', 'label':'123'},
    {"text": 'asd', 'label': '123'}]

strPattern = re.compile(r'"(.*)"')

testList = []
l = 1

for line in testT:
    # print(line)
    textAndLabel = dict()
    tmp = re.search(strPattern, line).group()
    tmp = re.sub(r'["|\,|\.|\(|\)]',"",tmp)
    textAndLabel['text'] = tmp
    textAndLabel['label'] = ""
    testList.append(textAndLabel)
    l += 1



json5.dump(testList,testJ, True,indent=2,trailing_commas=False)

testT.close()
testJ.close()