//: [Previous](@previous)

import Cocoa
import NaturalLanguage
import CreateML
import PlaygroundSupport


let data = try MLDataTable(contentsOf: URL(fileURLWithPath: "Users/zhongsuyang/Codes/Web/Web2020/exp2/dataset/train_off.json"))

let relationClassifier = try MLTextClassifier(trainingData: data,
                                              textColumn: "text",
                                              labelColumn: "label")
let trainingAccuracy = (1.0 - relationClassifier.trainingMetrics.classificationError) * 100
let validationAccuracy = (1.0 - relationClassifier.validationMetrics.classificationError)*100

let metaData = MLModelMetadata(author: "Suyuz", shortDescription: "Classify relation")
try relationClassifier.write(toFile: "~/Codes/Web/Web2020/exp2/models/relationClassifier.mlmodel")

var result = NSMutableString()
let testData = try MLDataTable(contentsOf: URL(fileURLWithPath: "Users/zhongsuyang/Codes/Web/Web2020/exp2/dataset/test.json"))

print(testData["text"][0])
for i in 0...1599 {
    let x = try relationClassifier.prediction(from: testData["text"][i])
    result.append(x)
    result.append("\n")
}
//let resultUrl = URL(fileURLWithPath: "Users/zhongsuyang/Codes/Web/Web2020/exp2/results/result_swift.txt")

try! result.write(to:URL(fileURLWithPath: "Users/zhongsuyang/Codes/Web/Web2020/exp2/results/swiftResult_perfect.txt"), atomically: true, encoding: String.Encoding.utf8.rawValue)


//: [Next](@next)
