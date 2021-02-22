import os
import pandas as pd
import numpy as np
from surprise import dump
from tqdm import tqdm

_, algoSVDBias = dump.load("../output/SVDbias.model")
_, algoSVDFunk = dump.load("../output/SVDFunk.model")
_, algoKNNBsl = dump.load("../output/KNN.model")
_, algoCoclus = dump.load("../output/Coclu.model")
_, algoBsl = dump.load("../output/bsl.model")

testData = pd.read_csv("../dataset/testing.dat", sep=',',
                       usecols=[0, 1], header=None, names=['user', 'item'])
print(testData)

fp = open("../output/result.txt", "w")
tmp= np.zeros(5)

for index, row in tqdm(testData.iterrows()):
    result1 = algoSVDBias.predict(row['user'], row['item'])[3]
    result2 = algoSVDFunk.predict(row['user'], row['item'])[3]
    result3 = algoKNNBsl.predict(row['user'], row['item'])[3]
    result4 = algoBsl.predict(row['user'], row['item'])[3]
    result5 = algoCoclus.predict(row['user'], row['item'])[3]
    # ans = result1
    ans = (result1+result2+result3+result4+result5)/5
    fp.write(str(round(ans)))
    # fp.write(str(random.randint(0,5)))
    fp.write('\n')

fp.close()
