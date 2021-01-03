from  simpletransformers.classification import ClassificationModel
import pandas as pd


model = ClassificationModel("roberta", "roberta-base", num_labels=10,use_cuda=False)

trainDf = pd.read_csv("../dataset/trainTransformers.csv", sep='\t')
print(trainDf)

model.train_model(trainDf,output_dir="../dataset/roberataFinetune")