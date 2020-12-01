import argparse
import re
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy import sparse
from nltk import stem


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, default="",
                        help='enter directly')
    parser.add_argument('--scan', action='store_true',
                        help='use keyboard input')
    parser.add_argument('--debug',action='store_true', default=False)

    opt = parser.parse_args()

    tokenList = []
    f = open("../output/df.txt")
    for t in f:  # 按行读取df文件，按序映射tokenList
        tokenList.append(t.split()[0])
    f.close()
    if opt.debug:
        tfidfPath = "../output/tf_idf_small.npz"
    else:
        tfidfPath = "../output/tf_idf.npz"
    if opt.scan:
        inQuery = input(
            "Please enter the query(any form like 'The president plans to contact the customers in the market'):\n")
    elif opt.query is not "":
        inQuery = opt.query
    else:
        inQuery = "The president plans to contact the customers in the market"
    
    print("\nWaiting for load the matrix")
    sparseMat = sparse.load_npz(tfidfPath)
    print("Successfuly load the matrix")
    # sparseMat = np.load(tfidfPath, allow_pickle=True)[()]
    # sparseMat = pd.read_csv(tfidfPath)
    tfidf = pd.DataFrame.sparse.from_spmatrix(sparseMat,index=tokenList)
    print(tfidf.head())

    stemmer = stem.SnowballStemmer('english')
    #Thing TODO to make enter
    listQuery = inQuery.split()
    vecQuery = pd.Series(np.zeros(tfidf.shape[0]), index=tokenList)
    for word in listQuery:
        if word in tokenList:
            vecQuery[stemmer.stem(word)] = 1
    print('\nQuery in vec is like')
    print(vecQuery)

    result = pd.Series(np.zeros(tfidf.shape[1]))
    for col in range(tfidf.shape[1]):
        vecD = np.array(tfidf[col])
        reD = np.sqrt(np.sum(vecD ** 2))
        if reD == 0:
            result[col] = 0
            continue
        reQ = np.sqrt(np.sum(np.array(vecQuery)**2))
        result[col] = np.sum(np.array(vecQuery) * vecD) / (reD * reQ)
        # if col == 305:
            # print(np.array(vecQuery))
            # print(vecD)
            # print(vecD * np.array(vecQuery))
            # print(np.sum(vecD * np.array(vecQuery)))
            # break

    result = result.sort_values(ascending=False)
    print('\n')
    # print(result[:10])

    resultDocIDs = np.array(result[:10].index) + 1
    print(resultDocIDs)

    print("The Top 10 answers and scores are:")
    paths = open("../dataset/path")
    docNum = 0
    numResult = 0
    for p in paths:
        docNum += 1
        if docNum in resultDocIDs:
            print(re.sub(r'\.\.\/dataset/', "", p.strip()) + "\nwith score: " + str(result[docNum - 1]))
            numResult+=1
        if numResult == 10:
            break
    paths.close()









