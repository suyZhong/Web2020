import numpy as np
import pandas as pd
import os
import re
from scipy.sparse import csr_matrix
from scipy import sparse

paths = open("../dataset/path")
docNum = 0
for p in paths:
    docNum += 1
print(docNum)
paths.close()

tokenDict = dict()
tokenList = []
idf = np.zeros(1000)
tokenID = 0
f = open("../output/df.txt") 
for t in f:  #按行读取df文件，按序映射token-ID
    tokenDict[t.split()[0]] = tokenID
    tokenList.append(t.split()[0])
    idf[tokenID] = int(t.split()[1])
    tokenID+=1
f.close()
print(tokenDict)

#计算idf
idf = np.log10(docNum/idf)

print(idf)
tf_idf = np.zeros(shape=(1000, docNum), order='C')


paths = open("../dataset/path")
docID = 0
print("begin construct tf")
for p in paths:
    docID += 1
    # if docID >= 1000:
        # break
    p = re.sub(r'\n', "", p)
    p = re.sub(r'\.\.\/dataset', "../dataset/tokenized", p)
    if os.path.isfile(p):
        f = open(p)
    else:
        continue

    try:
        tokens = f.readlines()
    except:
        print(p + ' can\'t be open!')
        f.close()
    else:
        for token in tokens:
            token = token.strip()
            if token in tokenDict:
                tf_idf[tokenDict[token]][docID - 1] += 1
        f.close()
print(tf_idf[0][:20])

print("begin calc tfidf")
for i in range(tf_idf.shape[0]):
    for j in range(tf_idf.shape[1]):
        if tf_idf[i][j] == 0:
            continue
        else:
            tf_idf[i][j] = (1 + np.log10(tf_idf[i][j])) * idf[i]
print(tf_idf[0][:15])

paths.close()
# tfidf_coo = sparse.coo_matrix(tf_idf); //可以为了CUDA去掉这行注释 以及下面那行savetxt
tf_idf = csr_matrix(tf_idf)
print(tf_idf[0])

# tf_idf
sparse.save_npz("../output/tf_idf.npz", tf_idf)
# np.savetxt("../output/tfidf_coo.txt",(tfidf_coo.data, tfidf_coo.row, tfidf_coo.col))
# sparse.save_npz("../output/tf_idf_small.npz", tf_idf) 
# np.save("../output/tf_idf.npz", tf_idf)

# tf_idf = pd.DataFrame(tf_idf, index=tokenList)

# tf_idf.to_csv('../output/tf_idf.csv')


