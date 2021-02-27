import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


trainData = pd.read_csv("../dataset/training.dat", sep=',', usecols=[
                        0, 1, 2, 3, 4], header=None, names=['user_id', 'mov_id', 'rating', 'timestamp', 'tag'])

allRatingMean = trainData['rating'].mean()

tagRating = trainData[['tag','rating']]
# print(pd.isna(trainData['tag']))
tagRating['tag'] = pd.isna(trainData['tag'])
print(tagRating['tag'].value_counts())
print(tagRating.groupby('tag')['rating'].value_counts())


print("观察刷零操作")
userTimeRating = trainData.groupby(['user_id', 'timestamp'])
userTimeRatingMean = userTimeRating['rating'].agg('mean')
print(userTimeRatingMean)
# print(userTimeRatingMean.xs(18).median())

# userTimeRatingMean.to_csv("../output/userTimeRatingMean.csv")
tagRating.groupby('tag')['rating'].value_counts().plot.bar()
# print(tagRating)
tagRatingMean = tagRating.groupby('tag').agg('mean')
plt.show()
# print(tagRatingMean)
