# extracting_from_review

4章の抽出ソースコードです。
日本語評価極性辞書と修論で使った映画レビューデータは格納していないので用意してください。
サンプルデータは格納しているので、そのデータで実行可能です。

## 環境
・ Python 3.5

[pipインストール一覧]

・ cabocha-python 0.69

・ mecab-python3 0.7  

## 実行方法
1. [ここ](http://www.cl.ecei.tohoku.ac.jp/index.php?Open%20Resources%2FJapanese%20Sentiment%20Polarity%20Dictionary)から、日本語評価極性辞書（用言編) と 日本語評価極性辞書（名詞編）をダウンロードしてdicフォルダに格納する

2. 映画レビューのデータを用意して、data/inputフォルダに格納する

3. python main.py input/data_sample.csv

4. レビュー解析結果が、data/outputフォルダに格納される


## ファイル構成

```
├── README.md
├── data
│   ├── input# 映画レビューデータ
│   │   mple_sample data.csv
│   └── output
├── dic# 日本語評価極性辞書
│   ├── pn.csv.m3.120408.trim# 日本語評価極性辞書（名詞編）ver.1.0（2008年12月版)
│   └── wago.121808.pn# 日本語評価極性辞書（用言編）ver.1.0（2008年12月版）
├── main.py# main関数
└── run_cabocha.py# 形態素解析処理

```