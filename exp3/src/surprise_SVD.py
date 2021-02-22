import os
import pandas as pd
import random
from surprise import SVD
from surprise import SVDpp
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise import dump
from surprise.model_selection import KFold
from tqdm import tqdm
from surprise.model_selection import GridSearchCV
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='run')
    opt = parser.parse_args()
    print(opt.mode)
    #direct read from file
    # reader = Reader(line_format='user item rating timestamp', sep=',')
    # data = Dataset.load_from_file("../dataset/training.dat", reader=reader)
    trainData = pd.read_csv("../dataset/training.dat", sep=',', usecols=[
                            0, 1, 2], header=None, names=['user_id', 'mov_id', 'rating'])
    print(trainData)
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(trainData[['user_id', 'mov_id','rating']], reader=reader)



    param_grid = {'n_factors': [100, 150, 50],
                  'reg_all': [0.05, 0.08]}
    # algo = SVD(biased=False)

    # algo = SVDpp(verbose=True) #TOO SLOW CANT FINISH
    # pred, algo = dump.load("../output/SVD")

    if opt.mode == 'grid':
         print("begin gridCV")
         gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3, joblib_verbose=2, n_jobs=2)
         gs.fit(data)
         algo = gs.algo_class()
        #  best RMSE score
         print(gs.best_score['rmse'])
        #  combination of parameters that gave the best RMSE score
         print(gs.best_params['rmse'])

    kf = KFold(n_splits=3)
    if opt.mode == 'grid':
        algo = SVD(reg_all=gs.best_params['rmse']['reg_all'], n_factors=gs.best_params['rmse']['n_factors'])
    else:
        algo = SVD(n_epochs=20, reg_all=0.08,verbose=True)
    print("begin fit and predict- KFold")
    for trainset, testset in tqdm(kf.split(data)):
        algo.fit(trainset)
        predictions = algo.test(testset)
        accuracy.rmse(predictions, verbose=True)
    dump.dump("../output/SVDFunk.model",algo=algo)

    # # trashy
    # trainset = data.build_full_trainset()
    # algo.fit(trainset)


    testData = pd.read_csv("../dataset/testing.dat", sep=',', usecols=[0, 1], header=None, names=['user', 'item'])
    print(testData)

    fp = open("../output/result.txt", "w")


    for index, row in tqdm(testData.iterrows()):
        result = algo.predict(row['user'], row['item'])
        fp.write(str(round(result[3])))
        # fp.write(str(random.randint(0,5)))
        fp.write('\n')

    fp.close()
