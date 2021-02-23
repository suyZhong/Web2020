import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

# fig, ax = plt.subplots()


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')

trainData = pd.read_csv("../dataset/training.dat", sep=',', usecols=[0, 1, 2, 3], header=None, names=['user_id', 'mov_id', 'rate', 'timestamp'])
testData = pd.read_csv("../dataset/testing.dat", sep=',',usecols=[0,1], header=None, names= ['user_id', 'mov_id'])

ratingMean = trainData['rate'].mean()
print(ratingMean)
# print("begin plot rating-cnt fig")
# rate = [0, 1, 2, 3, 4, 5]
# # rateCnt = trainData['rate'].value_counts()
# rateCnt = np.zeros(6,dtype=int)
# for i in trainData['rate']:
#     rateCnt[i] += 1
# print(rateCnt)
# label = 'rating'
# rects = plt.bar(rate, height=rateCnt, label=label)
# autolabel(rects)
# plt.title("rating-users bar")
# fig.tight_layout()
# plt.savefig("../figs/ratingCnt")
# plt.show()


# print("begin plot movie trend")
# fig, ax = plt.subplots()
# plt.title("movies")
# users = trainData['user_id'].value_counts()
# movies = trainData['mov_id'].value_counts(normalize=True)
# movIndex = np.arange(len(movies))
# rects = plt.plot(movIndex,movies)
# print(movies)
# # print(users)
# # movies.plot()
# # movies.plot.hist(bins=100)
# plt.grid(linestyle='-.')
# ax.set_xlabel("movies id ranked by popularity")
# ax.set_ylabel("normalize appearence rate")
# plt.savefig("../figs/movsCnt")
# plt.show()

# print("begin plot user-movi scatter")
# plt.title("user-mov scatter")

# # trainData.plot.scatter('user_id','mov_id',title="usermovi scat")
# plt.xlabel("user_id")
# plt.ylabel("mov_id")
# plt.scatter(trainData['user_id'], trainData['mov_id'], s = 0.5,label = 'trainData')
# plt.scatter(testData['user_id'], testData['mov_id'], c='red', s=0.5, label = 'testData')

# plt.savefig("../figs/user_mov")
# plt.show()

print("begin plot time trend")
timeRatingDf = pd.DataFrame(data=trainData[['timestamp','rate']])

timeRatingMeanDf = timeRatingDf.groupby('timestamp').agg('mean')
timeRatingMeanDf['delta']=timeRatingMeanDf['rate'].apply(lambda x: x-ratingMean)
timeRatingMeanDf.to_csv('../dataset/training_mean.dat')

timeRatingMeanDf.plot(label="time rate trend")
plt.xlabel("timestamp")
plt.ylabel("rate-mean")
plt.title("time rateMean trend")
plt.legend()
plt.grid(linestyle='-.')
plt.savefig("../figs/time_rate")
plt.show()


