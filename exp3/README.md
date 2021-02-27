## Environment

- MacBook Pro（16 英寸，2019）- i7 9750H - 16GB RAM
- macOS Catalina 10.15.7
- Xcode 12.1
- Python 3.7.4 with Anaconda3; using VS Code

## Requirement

```
surprise==0.1
pandas==0.25.1
scikit-learn==0.21.3
numpy==1.19.1
```

## Directory
```shell
.
├── README.md
├── dataset
│   ├── exp3_example_submission.txt
│   ├── relation.txt
│   ├── testing.dat
│   ├── training.dat
│   └── training_mean.dat
├── figs #图像
│   ├── 0.08reg.png
│   ├── dh_result.png
│   ...
│   └── usersCnt.png
├── output   #models 如果没有，bagging时需要先生成
│   ├── Coclu.model
│   ├── KNN.model
│   ├── KNNmean.model
│   ├── KNNzscore.model
│   ├── SVD.model
│   ├── SVDFunk.model
│   ├── SVDbias.model
│   ├── bsl.model
└── src
    ├── plot_data.py  #图像预处理生成
    ├── ran.py  #随机生成
    ├── surprise_KNN.py #KNN模型的生成和预测
    ├── surprise_SVD.py #SVD模型的生成和预测
    ├── surprise_bagging.py #集成学习
    ├── surprise_other.py #其他模型的生成和预测
    └── tag_analysis.py #分析标签
```

## TODO

- [x] just use SVD (1,2,3,5)
  - full dataset 2 is not good than K-Fold1
  - fault: !!! use `round()` not `int()` 3
  - PunkSVD not better than BiasSVD
  - SVDpp Too slow
  - KNNbsl (k=5)5
- [x] use boost (6)
  - SVD+KNN bagging linear 6 not good
    - perhaps not enough models...
  - SVD KNN baseline coclus 7 not good even
  - 01 should use mode not mean
- [x] use grid cv on SVD(4)
  - {'n_epochs': 10, 'lr_all': 0.005, 'reg_all': 0.04} 4
  - {'n_epochs': 20, 'lr_all': 0.005, 'reg_all': 0.06}
  - 1.2161151806697987
    - {'n_epochs': 20, 'reg_all': 0.08}
- [x] consider timestamp(8)

- [x] 很多零分项，出现于用户随机的个人行为，可能与当时评分的心情和时间等因素有关

