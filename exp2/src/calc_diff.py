f1 = open("../results/swiftResult.txt", "r")
# TODO
f2 = open("../dataset/dev_val_ans.txt", "r")

myAns = []
valAns = []

for l in f1:
    myAns.append(l)
f1.close()

for l in f2:
    valAns.append(l)
f2.close()

num = 1600
s = 0
for i in range(num):
    if valAns[i] == myAns[i]:
        s +=1

print(s/num)