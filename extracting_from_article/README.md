# extracting_from_review

5章と6章の抽出ソースコードです。

修論で使ったニュース記事データは格納していないので用意してください。

## 環境
・Python 3.5

・jupyter 4.1.0

[pipインストール一覧]

・pyknp 0.3

・scikit-learn 0.19.1

・pandas 0.23.1 

・sklearn-crfsuite 0.3.6

## 実行方法
1. bratでアノテーションしたデータをdata/inputフォルダに格納する

2. jupyter notebook

### ルールベースの実行方法
1. Ch5_Rule1_2.ipynb を開く

2. mode_idの値を変えることで、抽出方法1と2を変えることができる。

3. レビュー解析結果が、data/output/Chapter5フォルダに格納される

### CRFの実行方法(5章)
1. Ch5_Get_Juman_feature.ipynbを開いて実行してコーパス(corpus_5w1hs_ch5.txt)を作成する

2. Ch5_CRF.ipynbを開いて実行する

3. CRFの結果が、data/output/Chapter5フォルダに格納される

### CRFの実行方法(6章)
1. Ch6_Get_Juman_feature-bnst.ipynbを開いて実行してコーパス(corpus_5w1hs_ch6.txt)を作成する

2. Ch6_CRF.ipynbを開いて実行する

3. CRFの結果が、data/output/Chapter6フォルダに格納される

### 注意点

・ データを変更した場合は、データサイズの変更を忘れないようにしてください。

・ CRFのデータ番号と記事番号を合わせるためにdata_id.csvがあります。データを変更した場合は、data_id.csvの変更を忘れないようにしてください。

## ファイル構成

```
├── Ch5_CRF.ipynb# 5章のCRF
├── Ch5_Get_Juman_feature.ip # 5章のCRFコーパスを作成する
├── Ch5_Rule1_2.ipynb# 5章のルールベース
├── Ch6_CRF.ipynb# 6章のCRF
├── Ch6_Get_Juman_feature-bnst.ipynb# 6章のCRFコーパスを作成する
├── README.md
├── corpus_5w1hs_ch5.txt# 5章のCRFコーパス
├── corpus_5w1hs_ch6.txt# 6章のCRFコーパス
├── data
│   ├── input# アノテーションされたニュース記事
│   └── output# 抽出結果
│       ├── Chapter5
│       └── Chapter6
└── data_id.csv# CRFのデータ番号と記事番号
```

