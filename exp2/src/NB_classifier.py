import re
import nltk
import argparse
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import text


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




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float, default=1, help="NB hyperparam")
    parser.add_argument('--mode', type=str, default="dev", help="if test")
    opt = parser.parse_args()

    #read data and store
    trainTextList,labelList,entityList = readTrain(opt.mode)
    testTextList = readTest(opt.mode)

    # vectorizer = text.TfidfVectorizer(trainTextList, stop_words='english')
    vectorizer = text.TfidfVectorizer(trainTextList)
    trainVectors = vectorizer.fit_transform(trainTextList)
    testVectors = vectorizer.transform(testTextList)
    # print(trainVectors)

    # classifier = nltk.classify.NaiveBayesClassifier.train(zip(trainVectors, labelList))
    # result = classifier.classify_many(testVectors)
    classifier = MultinomialNB(0.1 - 0.0009 * opt.alpha)
    classifier.fit(trainVectors, labelList)
    
    result = classifier.predict(testVectors)
    fp = open("../results/nbResult.txt", "w")
    for i in result:
        fp.write(i)
        fp.write('\n')
    fp.close


    



