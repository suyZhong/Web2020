import os
import gensim
from gensim.models.doc2vec import TaggedDocument

import smart_open

def read_corpus(fname=str):
    with smart_open.open(fname) as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            yield TaggedDocument(tokens, [i])

trainData = list(read_corpus("../dataset/train.txt"))
testData = list(read_corpus("../dataset/test.txt"))

data = trainData + testData

model = gensim.models.doc2vec.Doc2Vec(vector_size=400, min_count=2, epochs=40)
model.build_vocab(data)

model.train(data, total_examples=model.corpus_count, epochs=model.epochs)

model.save("../models/model.d2v")


