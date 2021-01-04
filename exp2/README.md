## Environment

- MacBook Pro（16 英寸，2019）- i7 9750H - 16GB RAM
- macOS Catalina 10.15.7
- Xcode 12.1
- Python 3.7.4 with Anaconda3; using VS Code

## Requirement

```
simpletransformers==0.51.9
nltk==3.4.5
gensim==3.8.3
pandas==0.25.1
scikit-learn==0.21.3
numpy==1.19.1
```

## Directory

```shell
├── README.md
├── dataset	//数据集目录
├── figs		//图片目录
├── models	//存放模型的目录，只保留swift的模型（其他的太大了）
│   ├── dev_relationClassifier.mlmodel
│   └── relationClassifier.mlmodel
├── results	//结果的目录
├── src
│   ├── NER.py	//使用RoBERTa进行关系抽取和实体识别的文件
│   ├── NER_roberta_model.py	//产生上述模型的文件
│   ├── calc_diff.py	//测试正确性时的文件
│   ├── classifier.py	//分类任务
│   ├── classifier_roberta_model.py	//产生分类模型
│   ├── doc2v.py	//产生doc2vec模型
│   ├── gen_dataset.py	//划分自己数据集的模型
│   ├── relation_classifier.playground	//swift模型
│   │   ├── Pages
│   │   │   ├── classifier.xcplaygroundpage
│   │   │   │   ├── Contents.swift	//代码文件
│   │   │   │   └── timeline.xctimeline
│   │   │   └── dev_classifier.xcplaygroundpage
│   │   │       ├── Contents.swift	//代码文件
│   │   │       └── timeline.xctimeline
│   ├── runs	//tensorboard文件
│   ├── train.sh	//自己循环训练的脚本
│   ├── txt2CoNLL.py	//产生CoNLL格式数据集
│   ├── txt2baidu.py	//产生百度EasyDL格式数据集
│   ├── txt2csv.py	//产生csv格式
│   ├── txt2json_test.py	//产生swift json格式
│   ├── txt2json_train.py	//同上
│   └── txt2txt.py	//产生baidu分类格式
└── 实验报告.md
```

## Run

Swift分类任务：

- 打开Xcode
- 打开`relation_classifier.playground`
- 点击左边竖栏蓝色按钮

`classifier.py`

普通分类（Naive_Bayes，SGD）普通特征（Tf-iDF，OneHot）

```shell
cd src/
python classifier.py --mode result --method SGD
```

- `--mode`为"dev"时启用测试模式
- `--method`为"NB"，"SGD"分别为两种分类方法
- 默认使用tfidf向量，如果要切换，麻烦自己去下注释（

使用doc2v.py生成doc2vec向量

```shell
python doc2v.py
```

simpletransformer分类：

```shell
cd src/
python classifier_roberta.py  #如果有CUDA，将代码中use_cuda设置为True
python classifier.py --mode result --method ROBERTA
```

NER任务：（需要先建立classifier_roberta模型）

```shell
cd src/
cp -r outputs ../model/class_outputs
python NER_roberta_model.py
python NER.py
```

