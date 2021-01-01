import os
import re
import random

# f = open("../dataset/train.txt", 'r')
f = open("/Users/zhongsuyang/Downloads/train.txt", 'r')
l = 1
dev_train = []
dev_val = []
dev_val_ans =[]

ratio = 0.8
trainLines = 8000 * 2

for line in f:
    if l > ratio * trainLines:
        if l % 2 == 1:
            dev_val.append(line)
        elif l % 2 == 0:
            relation = re.match(r"([a-zA-Z]|\-)*", line).group()
            dev_val_ans.append(relation)
    else:
        dev_train.append(line)
    l +=1


f.close()

fTrain = open("../../../dev_train.txt", 'w')
for i in dev_train:
    fTrain.write(i)
fTrain.close()

fVal = open("../../../dev_val.txt", 'w')
for i in dev_val:
    fVal.write(i)
fVal.close()

fValAns = open("../../../dev_val_ans.txt", 'w')
for i in dev_val_ans:
    fValAns.write(i)
    fValAns.write('\n')
fValAns.close()
