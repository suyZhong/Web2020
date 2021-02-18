import random
import pandas as pd
from tqdm import tqdm


testData = pd.read_csv("../dataset/testing.dat", sep=',',
                       usecols=[0, 1], header=None, names=['user', 'item'])
print(testData)

fp = open("../output/result.txt", "w")


for index, row in tqdm(testData.iterrows()):
    fp.write(str(random.randint(0, 5)))
    fp.write('\n')
