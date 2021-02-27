import os
import pandas as pd
import numpy as np
from surprise import dump
from tqdm import tqdm

trainRatingMean = 2.5732511874
tagTrueMean = 2.891059
tagFalseMean = 2.316351

_, algoSVDBias = dump.load("../output/SVDbias.model")
_, algoSVDFunk = dump.load("../output/SVDFunk.model")
_, algoKNNBsl = dump.load("../output/KNN.model")
_, algoCoclus = dump.load("../output/Coclu.model")
_, algoBsl = dump.load("../output/bsl.model")
_, algoKNNmean = dump.load("../output/KNNmean.model")
_, algoKNNzscore = dump.load("../output/KNNzscore.model")
testData = pd.read_csv("../dataset/testing.dat", sep=',',
                       usecols=[0, 1, 2, 3], header=None, names=['user', 'item', 'timestamp', 'tag'])
print(testData)
print(testData['timestamp'].value_counts())
trainData = pd.read_csv("../dataset/training.dat", sep=',', usecols=[
                        0, 1, 2, 3, 4], header=None, names=['user_id', 'mov_id', 'rating', 'timestamp', 'tag'])
print(trainData)

tmp = np.zeros(5)

avgRating = trainRatingMean
zeroRating = 0
timeChange = 0
zeross = 0
userid = 0
results = []
curTime = '2011-01'
timeFlag = True
userTimeRating = trainData.groupby(['user_id', 'timestamp'])
userTimeRatingMean = userTimeRating['rating'].agg('mean')

for index, row in tqdm(testData.iterrows()):
    userid = row['user']
    itemid = row['item']
    voteArray = np.zeros(5)
    if row['timestamp'] != curTime:
        curTime = row['timestamp']
        try:
            avgRating = userTimeRatingMean.xs(row['user']).loc[curTime]
        except KeyError:
            # avgRating = userTimeRatingMean.xs(row['user']).median()
            avgRating = trainRatingMean
        timeChange+=1

    voteArray[0] = algoSVDBias.predict(userid, itemid)[3]
    voteArray[1] = algoSVDFunk.predict(userid, itemid)[3]
    voteArray[2] = algoKNNBsl.predict(userid, itemid)[3]
    voteArray[3] = algoBsl.predict(userid, itemid)[3]
    voteArray[4] = algoCoclus.predict(userid, itemid)[3]
    # mean
    ans = voteArray.mean()

    if avgRating <= 1.0 and ans <=3:
        zeroRating +=1
        results.append(0)
    else:
        roundArray = np.round(voteArray).astype(int)
        counts = np.bincount(roundArray)
        results.append(np.argmax(counts))
    # fp.write(str(random.randint(0,5)))

print("zeroRatings ",zeroRating)
print(timeChange)
print(zeross)
resultDf = pd.DataFrame(results, columns=['rating'])
resultDf.to_csv("../output/result.txt", header=None, index=False)
