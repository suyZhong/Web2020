import Cocoa
import NaturalLanguage
import CreateML
import PlaygroundSupport


let data = try MLDataTable(contentsOf: URL(fileURLWithPath: "Users/zhongsuyang/Codes/Web/Web2020/exp2/dataset/train.json"))
let (trainingData, testingData) = data.randomSplit(by: 0.7, seed: 5)

let relationClassifier = try MLTextClassifier(trainingData: trainingData,
                                              textColumn: "text",
                                              labelColumn: "label")
let trainingAccuracy = (1.0 - relationClassifier.trainingMetrics.classificationError) * 100
let validationAccuracy = (1.0 - relationClassifier.validationMetrics.classificationError)*100

let evaluationMetrics = relationClassifier.evaluation(on: testingData, textColumn: "text", labelColumn: "label")

let evaluationAccuracy = (1.0 - evaluationMetrics.classificationError) * 100
print("evaluationAccuracy is ")
print(evaluationAccuracy)

let modelURL = playgroundSharedDataDirectory
let metaData = MLModelMetadata(author: "Suyuz", shortDescription: "Classify relation")
try relationClassifier.write(toFile: "Users/zhongsuyang/Codes/Web/Web2020/exp2/models/dev_relationClassifier.mlmodel")

