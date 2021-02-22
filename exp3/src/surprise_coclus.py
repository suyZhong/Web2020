import os
import pandas as pd
from surprise import CoClustering
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise import dump
from surprise.model_selection import KFold
from tqdm import tqdm

# #direct read from file
# reader = Reader(line_format='user item rating timestamp', sep=',')
# data = Dataset.load_from_file("../dataset/training.dat", reader=reader)

trainData = pd.read_csv("../dataset/training.dat", sep=',', usecols=[
                        0, 1, 2], header=None, names=['user_id', 'mov_id', 'rating'])
print(trainData)
reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(trainData[['user_id', 'mov_id','rating']], reader=reader)

kf = KFold(n_splits=3)
algo = CoClustering(n_cltr_i=5)
# pred, algo = dump.load("../output/SVD")

print("begin fit and predict")
for trainset, testset in tqdm(kf.split(data)):
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions, verbose=True)

# # trashy
# trainset = data.build_full_trainset()
# algo.fit(trainset)

dump.dump("../output/Coclu.model",algo=algo)

testData = pd.read_csv("../dataset/testing.dat", sep=',', usecols=[0, 1], header=None, names=['user', 'item'])
print(testData)

fp = open("../output/result.txt", "w")


for index, row in tqdm(testData.iterrows()):
    result = algo.predict(row['user'], row['item'])
    fp.write(str(round(result[3])))
    fp.write('\n')
