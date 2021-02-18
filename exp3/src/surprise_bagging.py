import os
import pandas as pd
from surprise import dump
from tqdm import tqdm

_, algoSVDBias = dump.load("../output/SVDbias.model")
_, algoSVDFunk = dump.load("../output/SVDFunk.model")
_, algoKNNBsl = dump.load("../output/KNN.model")

testData = pd.read_csv("../dataset/testing.dat", sep=',',
                       usecols=[0, 1], header=None, names=['user', 'item'])
print(testData)

fp = open("../output/result.txt", "w")

for index, row in tqdm(testData.iterrows()):
    result1 = algoSVDBias.predict(row['user'], row['item'])
    result2 = algoSVDFunk.predict(row['user'], row['item'])
    result3 = algoKNNBsl.predict(row['user'], row['item'])
    ans = (result1[3]+result2[3]+result3[3])/3
    fp.write(str(round(ans)))
    # fp.write(str(random.randint(0,5)))
    fp.write('\n')

fp.close()
