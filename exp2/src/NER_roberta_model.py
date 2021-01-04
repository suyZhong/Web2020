import pandas as pd
from simpletransformers.ner import NERModel, NERArgs

relationLabels = ["O","B-CAUSE-EFFECT", "I-CAUSE-EFFECT", "B-COMPONENT-WHOLE", "I-COMPONENT-WHOLE",
 "B-ENTITY-DESTINATION", "I-ENTITY-DESTINATION", "B-PRODUCT-PRODUCER", "I-PRODUCT-PRODUCER", "B-ENTITY-ORIGIN",
                  "I-ENTITY-ORIGIN", "B-MEMBER-COLLECTION", "I-MEMBER-COLLECTION", "B-MESSAGE-TOPIC",
                  "I-MESSAGE-TOPIC", "B-CONTENT-CONTAINER", "I-CONTENT-CONTAINER", "B-INSTRUMENT-AGENCY",
                  "I-INSTRUMENT-AGENCY", "B-OTHER", "I-OTHER"]
modelArg = NERArgs()
modelArg.labels_list = relationLabels

model = NERModel("roberta", "./outputs/", labels=relationLabels,use_cuda=False, args=modelArg)

trainDf = pd.read_csv("../dataset/trainNER.csv", sep='|')
print(trainDf)

model.train_model(trainDf, output_dir="../models/roberataNER")
