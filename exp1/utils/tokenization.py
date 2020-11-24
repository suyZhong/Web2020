from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import stem
import read_file
import os

sentence = """
    I am superman, but I want to be the Peter Pan.
    USTC is the best university in Hefei.
    He has many cats, and I would like flying kites.
    """

sentences = ['I am superman, but I want to be the Peter Pan.',
             'USTC is the best university in Hefei.',
             'He has many cats, and I would like flying kites.',
             'The Conventions of a number of the States having, at the time of adopting the Constitution, expressed a desire, in order to prevent misconstruction or abuse of its powers, that further declaratory and restrictive clauses should be added, and as extending the ground of public confidence in the Government will best insure the beneficent ends of its institution;']



stopWords = set(stopwords.words('english'))
stemmer = stem.SnowballStemmer('english')
docID = 0
invertIndex = dict()
paths=open("../dataset/path")

for p in paths:
    p=p.replace("\n","")
    f = open(p)
    content = f.read()
    tokens = word_tokenize(content)
    # 去除停用词操作
    tokensFiltered = []
    for token in tokens:
        if token not in stopWords:
            tokensFiltered.append(token)

    #词根化操作
    stemmedTokens = []
    for token in tokensFiltered:
        stemmedTokens.append(stemmer.stem(token))
    
    #构建倒排索引（循环每个文档，不断加入）
    for token in stemmedTokens:
        if token not in invertIndex:
            invertIndex[token]= [docID]
        elif docID not in invertIndex[token]:
            invertIndex[token].append(docID)
    docID += 1
    f.close()

print(tokens)
print(tokensFiltered)
print(stemmedTokens)
print(invertIndex)
