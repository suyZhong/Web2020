## Environment

- MacBook Pro（16 英寸，2019）- i7 9750H - 16GB RAM
- macOS Catalina 10.15.7
- Xcode 12.1
- Python 3.7.4 with Anaconda3; using VS Code

## TODO

- [x] just use SVD (1,2,3,5)
  - full dataset 2 is not good than K-Fold1
  - fault: !!! use `round()` not `int()` 3
  - PunkSVD not better than BiasSVD
  - SVDpp Too slow
  - KNNbsl 5
- [x] use boost (6)
  - SVD+KNN bagging linear 6 not good
    - perhaps not enough models...
- [x] use grid cv on SVD(4)
  - {'n_epochs': 10, 'lr_all': 0.005, 'reg_all': 0.04} 4
  - {'n_epochs': 20, 'lr_all': 0.005, 'reg_all': 0.06}
  - 1.2161151806697987
    - {'n_epochs': 20, 'reg_all': 0.08}

