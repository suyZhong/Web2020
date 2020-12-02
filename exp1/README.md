## Environment

- MacBook Pro（16 英寸，2019）- i7 9750H - 16GB RAM
- macOS Catalina 10.15.7
- Python 3.7.4 with Anaconda3; using VS Code

## Requirements

除了anaconda环境提供外，没有额外的包。可能需要配置nltk：

```python
import nltk
nltk.download()
```

经测试：本机pandas==0.25.1，可能需要pandas>=0.25.1版本

## Tutorial 

最好在Linux~~「没试过」~~「试过了（CentOS）」或Mac上测试

#### 布尔查询

```shell
> cd exp1/src
> python bool_search.py --query "power&businessORenergy & natural AND signed"
 ...
```

- 会把输出直接`print()`推荐重定向到文件（我自己就是这么做的）
- 可接受两个输入参数：
  - `--query "布尔查询字符串"`
  - `--scan` 带有这个参数时，将从键盘获取输入
- 字符串接受类似正则表达式" [NOT|$\varepsilon$] **token**'(' [AND|OR|'|'|'&'] [NOT|$\varepsilon$]**token**')' +"的格式
  - NOT AND OR优先级依次递减，也可以用&｜！。
  - 若要NOT掉一串词，需要对其打括号

#### Tf-idf语义查询

```shell
> cd exp1/src
> python semantic_search.py --query "The president plans to contact customers in the market"
 ...
```

- 可接受三个输入参数：
  - `--query "布尔查询字符串"`
  - `--scan ` 同上
  - `--debug` 输入的tf-idf矩阵是一个1000x1000的小矩阵
- 接受的输入为查询词组，以空格隔开

## Introduction

##### 文件建立

首先使用`utils/read_file.py`对maildir文件夹进行递归搜索，并生成\<docID-path\>对应表，存放在dataset/里

然后使用`utils/tokenization_opt.py`对`dataset/path`进行遍历，对每个文档依次进行，正则化，分词，去停用词，词根化，获取分词后的文档「在后续实验中，选择将其存储，以便生成tf-idf」，然后遍历这个文档的词进行倒排表的建立，倒排表存储在`output/`里面

使用`utils/matrix.py`对之前存储的分词结果进行遍历，并建立tf-idf矩阵，使用scipy中的sparse进行矩阵压缩，将压缩后的.npz文件存储在`output/`里

##### 检索

使用`bool_search.py`实现布尔检索，经过将输入其转化为逆波兰表达式的形式，然后输出为符合条件文档的相对路径（会直接print在终端），所以请谨慎。

使用`semantic_search.py`实现语义检索。首先原矩阵解压并读取在内存中（耗时），然后经过欧式归一化以及余弦相似度计算出各文档得分情况，并排序以及输出。

## Directory

提交压缩包里，本顶层目录下共有五个文件夹：

```shell
├── README.md
├── dataset
│   ├── path	//<docID-文档路径>对
│   └── tokenized	//空文件夹，存放分词后的文档
├── exp1.pdf	//实验文档
├── figs	//实验报告与README图片来源
├── output						
│   ├── df.txt	//存放前一千个词项对应的df
│   ├── index.txt	//存放倒排表
│   ├── tf_idf.npz	//存放使用scipy.sparse压缩的tf-idf矩阵
│   ├── some logs
│   └── tf_idf_small.npz	//存放1000x1000的debug矩阵
├── src
│   ├── bool_search.py	//布尔查询
│   └── semantic_search.py	//语义查询
├── utils
│   ├── read_file.py	//用来生成path对的文件
│   ├── matrix.py	//用来生成tf-idf的文件
│   ├── tokenization.py	//用来生成倒排表的优化前文件
│   └── tokenization_opt.py	//优化后的生成倒排表的文件
└── 实验文档.md
```


