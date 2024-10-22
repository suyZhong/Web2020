from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import stem
import read_file
import os
import re

sentences = ['I am superman, but I want to be the Peter Pan.',
             'USTC is the best university in Hefei.',
             'He has many cats, and I would like flying kites.',
             'The Conventions of a number of the States having, at the time of adopting the Constitution, expressed a desire, in order to prevent misconstruction or abuse of its powers, that further declaratory and restrictive clauses should be added, and as extending the ground of public confidence in the Government will best insure the beneficent ends of its institution;']

mailStopwords = ['com', 'http', 'enron', 'the', 'hou', 'thank', 'subject','nbsp', 'pm', 'am', 'th']
stopWords = set(stopwords.words('english'))
stopWords = stopWords.union(mailStopwords)
stemmer = stem.SnowballStemmer('english')


docID = int(1)

docIndex = dict()
invertIndex = dict()
tokenDF = dict()
tokenAllTF = dict()
paths = open("../dataset/path")

#用于正则表达式的Patterns
headPattern = re.compile(
    r'Message-ID|Date:|From:|To:|Mime\-Version|Content\-Type|Content-Transfer-Encoding|X\-[a-zA-Z]*|Bcc:|Cc:|cc:')
otherPattern = re.compile(r'[^a-zA-Z\s]+')
mailPattern = re.compile(r'[a-zA-Z0-9]+((\.[a-zA-Z0-9]+)|(@[a-zA-Z0-9]+))+')
# urlPattern = re.compile(r'http:/[.]*\s')
htmlPattern = re.compile(r'\<[^\>]+\>')
charaPattern = re.compile(r' [a-zA-Z] ')

for p in paths:
    if docID != 13676:
        docID+=1
        continue
    # if docID >= 20000:
    #     break
    p = re.sub(r"\n", "", p)
    f = open(p)
    try:
        content = f.readlines()
    except:
        print(p)
        f.close()
    else:
        reContent = []
        for l in content:
            if re.match(headPattern, l):    #消除除了subject外的邮件头部
                continue
            else:
                reContent.append(l)
        stringContent = ''.join(reContent)
        print(str(stringContent)+"\n------!@)#*)(@!*#)(@!*)#-------------\n\n\n")
        noMailWords = re.sub(mailPattern, " ", str(stringContent))  # 去掉mail
        noHtmlWords = re.sub(htmlPattern, " ", noMailWords)
        words = re.sub(otherPattern, " ", noHtmlWords)  # 去掉其余东西
        noSingleCharaWords = re.sub(charaPattern, " ", words)
        print(words+"\n-------------!@#*&#)$&)@!(#*@)!(#*)@------\n\n\n")
        tokens = word_tokenize(noSingleCharaWords)
        # 去除停用词操作
        tokensFiltered = []
        for token in tokens:
            if token not in stopWords:
                tokensFiltered.append(token)

        # 词根化操作
        stemmedTokens = []
        for token in tokensFiltered:
            stemmed = stemmer.stem(token)
            # stemmedTokens.append(stemmed)
            if stemmed not in stopWords:
                stemmedTokens.append(stemmed)

        # 构建倒排索引（循环每个文档，不断加入）
        # for token in stemmedTokens:
        #     if token not in invertIndex:
        #         invertIndex[token] = [docID]
        #     elif docID not in invertIndex[token]:
        #         invertIndex[token].append(docID)


        for token in stemmedTokens:
            if token in tokenAllTF:
                tokenAllTF[token] += 1
            else:
                tokenAllTF[token] = 1
            if token in invertIndex:
                if docID not in invertIndex[token]:
                    invertIndex[token].append(docID)
                    tokenDF[token] += 1
            else:
                invertIndex[token] = [docID]
                tokenDF[token] = 1
        # for token in stemmedTokens:
        #     if token in invertIndex:
        docID += 1
        f.close()



# print(tokens)
# print(tokensFiltered)
# print(stemmedTokens)
# print(str(invertIndex.keys))
# print(tokenDF)

sortInvertIndex = sorted(invertIndex, key=lambda i: tokenAllTF[i], reverse=True)
mode = "debug"
output = "../output/invert_" + mode + ".txt"
f = open(output, "w")

num = 1000
for d in sortInvertIndex:
    if num <= 0:
        break
    f.write(d)
    f.write(" ")
    f.write(str(invertIndex[d]))
    f.write('\n')
    num-=1
f.close()
