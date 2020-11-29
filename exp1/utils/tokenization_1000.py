from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import stem
import read_file
import os
import re
import time

sentences = ['I am superman, but I want to be the Peter Pan.',
             'USTC is the best university in Hefei.',
             'He has many cats, and I would like flying kites.',
             'The Conventions of a number of the States having, at the time of adopting the Constitution, expressed a desire, in order to prevent misconstruction or abuse of its powers, that further declaratory and restrictive clauses should be added, and as extending the ground of public confidence in the Government will best insure the beneficent ends of its institution;']

mailStopwords = ['com', 'http', 'enron', 'the', 'hou',
                 'thank', 'subject', 'nbsp', 'pm', 'am', 'th']
stopWords = set(stopwords.words('english'))
stopWords = stopWords.union(mailStopwords)
stemmer = stem.SnowballStemmer('english')


docID = int(1)

docIndex = dict()
invertIndex = dict()
tokenDF = dict()
tokenAllTF = dict()
tokenTF = dict()
paths = open("../dataset/path")

# 用于正则表达式的Patterns
headPattern = re.compile(
    r'Message-ID|Date:|From:|To:|Mime\-Version|Content\-Type|Content-Transfer-Encoding|X\-[a-zA-Z]*|Bcc:|Cc:|cc:')
otherPattern = re.compile(r'[^a-zA-Z\s]+')
mailPattern = re.compile(r'[a-zA-Z0-9]+((\.[a-zA-Z0-9]+)|(@[a-zA-Z0-9]+))+')
# urlPattern = re.compile(r'http:/[.]*\s')
htmlPattern = re.compile(r'\<[^\>]+\>')
charaPattern = re.compile(r' [a-zA-Z] ')

print("\n\n")
reTime = 0
indexTime = 0
stopTime = 0
stemTime = 0
start_time = time.time()
for p in paths:
    # if docID != 13676:
    #     docID+=1
    #     continue
    if docID >= 40000:
        break
    p = re.sub(r"\n", "", p)
    f = open(p)
    try:
        content = f.readlines()
    except:
        print(p)
        f.close()
    else:
        # 正则阶段不耗时。。。
        start = time.time()
        reContent = []
        for l in content:
            if re.match(headPattern, l):  # 消除除了subject外的邮件头部
                continue
            else:
                reContent.append(l)
        stringContent = ''.join(reContent)
        # print(str(stringContent)+"\n------!@)#*)(@!*#)(@!*)#-------------\n\n\n")
        noMailWords = re.sub(mailPattern, " ", str(stringContent))  # 去掉mail
        noHtmlWords = re.sub(htmlPattern, " ", noMailWords)
        words = re.sub(otherPattern, " ", noHtmlWords)  # 去掉其余东西
        noSingleCharaWords = re.sub(charaPattern, " ", words)
        # print(words+"\n-------------!@#*&#)$&)@!(#*@)!(#*)@------\n\n\n")
        end = time.time()
        reTime += end-start

        start = time.time()
        tokens = word_tokenize(noSingleCharaWords)
        stemmedTokens = []
        for token in tokens:
            if token not in stopWords:
                stemmedToken = stemmer.stem(token)
                if stemmedToken not in stopWords:
                    stemmedTokens.append(stemmedToken)
        end = time.time()
        stemTime += end-start

        # 构建倒排索引（循环每个文档，不断加入）
        # for token in stemmedTokens:
        #     if token not in invertIndex:
        #         invertIndex[token] = [docID]
        #     elif docID not in invertIndex[token]:
        #         invertIndex[token].append(docID)

        # start = time.time()
        # for token in stemmedTokens:
        #     if token in tokenAllTF:
        #         tokenAllTF[token] += 1
        #     else:
        #         tokenAllTF[token] = 1
        #     if token in invertIndex:
        #         if docID not in invertIndex[token]:
        #             invertIndex[token].append(docID)
        #             tokenDF[token] += 1
        #     else:
        #         invertIndex[token] = [docID]
        #         tokenDF[token] = 1
        # end = time.time()
        # indexTime += end - start

        docIndex[docID] = []
        start = time.time()
        for token in stemmedTokens:
            if token in tokenAllTF:
                tokenAllTF[token] += 1
            else:
                tokenAllTF[token] = 1
            if token not in docIndex[docID]:
                docIndex[docID].append(token)
        end = time.time()
        indexTime += end - start
        docID += 1
        f.close()


end_time = time.time()




# print(tokens)
# print(tokensFiltered)
# print(stemmedTokens)
# print(str(invertIndex.keys))
# print(tokenDF)

# sortInvertIndex = sorted(
#     invertIndex, key=lambda i: tokenAllTF[i], reverse=True)
mode = "debug"
output = "../output/invert_" + mode + ".txt"
f = open(output, "w")

start = time.time()
num = 0
sortToken = sorted(tokenAllTF, key=lambda i: tokenAllTF[i], reverse=True)
for i in sortToken:
    if num >= 1000:
        break
    # f.write(i)
    invertIndex[i] = []
    for doc in docIndex:
        if i in docIndex[doc]:
            invertIndex[i].append(doc)
    num+=1
# f.close()
end = time.time()
changeTime = end -start


num = 1000
for t in invertIndex:
    if num <= 0:
        break
    f.write(t)
    f.write(" ")
    for d in invertIndex[t]:
        f.write(str(d)+' ')
    f.write('\n')
    num -= 1
f.close()

print('total docs = ' + str(docID))
print('total time = ' + str(end_time - start_time))
print('index time = ' + str(indexTime))
print('reTime = '+str(reTime))
print('stopTime = ' + str(stopTime))
print('stemTime = ' + str(stemTime))
print('changeTime = '+ str(changeTime))
