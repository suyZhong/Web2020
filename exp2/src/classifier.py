import re
import nltk
import argparse
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import text
from sklearn.linear_model import SGDClassifier
import gensim
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from simpletransformers.classification import ClassificationModel


relationClasses = ['Cause-Effect', 'Component-Whole', 'Entity-Destination',
                   'Product-Producer', 'Entity-Origin',
                   'Member-Collection', 'Message-Topic',
                   'Content-Container', 'Instrument-Agency', 'Other']

# 三种数据格式
textPattern = re.compile(r'"(.*)"')
relationPattern = re.compile(r"([a-zA-Z\-]*)")
entityPattern = re.compile(r"\((.*)\)")


def readTrain(mode=str):
    textList = []
    labelList = []
    entityList = []
    filename = "train.txt"
    if mode == "dev":
        filename = "dev_"+filename
    else:
        pass
    filename = "../dataset/" + filename
    fp = open(filename, "r")
    l = 1
    for line in fp:
        if l % 2 == 1:
            text = re.search(textPattern, line).group()
            text = re.sub(r'["|\,|\.|\(|\)]', "", text)
            textList.append(text)
        else:
            label = re.match(relationPattern, line).group()
            labelList.append(label)
            searchObj = re.search(r"\((.*)\)", line)
            ens = re.sub(r"\(|\)", "", searchObj.group())
            entities = ens.split(",", maxsplit=1)
            entityList.append(entities)
        l += 1
    fp.close()
    return textList, labelList, entityList


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


def get_onehot_feature(dataList=list, featureWords=list):
    # features = np.ndarray((1,len(featureWords)))
    features = []
    for text in dataList:
        text_words = nltk.word_tokenize(text)
        vec = []
        for i in range(0, len(featureWords)):
            if featureWords[i] in text_words:
                vec.append(1)
            else:
                vec.append(0)
        features.append(vec)
    return features


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float, default=1, help="NB hyperparam")
    parser.add_argument('--mode', type=str, default="dev", help="if test")
    parser.add_argument('--method', type=str, default="SGD",
                        help="choose classifier")
    opt = parser.parse_args()

    # read data and store
    f2 = open("../dataset/dev_test_ans.txt", "r")
    valAns = []
    for l in f2:
        l = re.sub("\n", "", l)
        valAns.append(l)
    f2.close()
    print(valAns[:10])
    trainTextList, labelList, entityList = readTrain(opt.mode)
    testTextList = readTest(opt.mode)

    entities = []
    for en in entityList:
        entities.append(en[0])
        entities.append(en[1])

    featureList = list(set(entities))

    #获取onehot 但是太拉垮了
    # trainOneHotVec = get_onehot_feature(trainTextList, featureList)
    # testOneHotVec = get_onehot_feature(testTextList, featureList)

    # vectorizer = text.TfidfVectorizer(trainTextList, stop_words='english')
    vectorizer = text.TfidfVectorizer(trainTextList)
    trainVectors = vectorizer.fit_transform(trainTextList)
    testVectors = vectorizer.transform(testTextList)
    # print(trainVectors)

    #doc2vec
    d2vmodel = Doc2Vec.load("../models/model.d2v")
    trainDoc2Vec = []
    print(trainTextList[0].lower().split())
    print(gensim.utils.simple_preprocess(trainTextList[0]))
    for string in trainTextList:
        string = gensim.utils.simple_preprocess(string)
        trainDoc2Vec.append(d2vmodel.infer_vector(string))
    testDoc2Vec = []
    for string in testTextList:
        string = gensim.utils.simple_preprocess(string)
        testDoc2Vec.append(d2vmodel.infer_vector(string))


    # classifier = nltk.classify.NaiveBayesClassifier.train(zip(trainVectors, labelList))
    # result = classifier.classify_many(testVectors)
    # train and val
    if(opt.mode == "dev"):
        step = int(opt.alpha)
        for i in range(step):
            if opt.method == "NB":
                classifier = MultinomialNB(1 - 0.009 * i)
            elif opt.method == "SGD":
                classifier = SGDClassifier(loss='log')
            classifier.fit(trainVectors, labelList)
            # classifier.fit(trainOneHotVec, labelList)
            classifier.fit(trainDoc2Vec, labelList)
            # result = classifier.predict(testVectors)
            # result = classifier.predict(testOneHotVec)
            result = classifier.predict(testDoc2Vec)
            num = 1600
            s = 0
            maxS = -1
            for i in range(num):
                if valAns[i] == str(result[i]):
                    s += 1
            if maxS <= s:
                maxS = s
                maxResult = result
            print(s / num)
    else:
        if opt.method == "NB":
            classifier = MultinomialNB(1 - 0.009 * opt.alpha)
            classifier.fit(trainDoc2Vec, labelList)
            maxResult = classifier.predict(testDoc2Vec)
        elif opt.method == "SGD":
            classifier = SGDClassifier()
            classifier.fit(trainDoc2Vec, labelList)
            maxResult = classifier.predict(testDoc2Vec)
        elif opt.method == "ROBERTA":
            model = ClassificationModel(
                "roberta", "./outputs", use_cuda=False)
            predict, rawOut = model.predict(testTextList)
            # predict, rawOut = model.predict(
            #     ["The body of her nephew was in a suitcase under the bed"])
            maxResult=[]
            for i in predict:
                maxResult.append(relationClasses[i])

        # classifier.fit(trainOneHotVec, labelList)
        # maxResult = classifier.predict(testOneHotVec)
        # maxResult = classifier.predict(testVectors)

    print(maxResult)
    fp = open("../results/stResult.txt", "w")
    for i in maxResult:
        fp.write(i)
        fp.write('\n')
    fp.close()
