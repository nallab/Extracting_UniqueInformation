#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re
import datetime
import run_cabocha

argvs = sys.argv
argc = len(argvs)

# 引数チェック
if (argc != 2):
    print ('prease type "python %s reviewfile"'%argvs[0])
    sys.exit()

if __name__ == "__main__":

    # 入力: レビューファイルの読み込み
    input_f = open(argvs[1])
    Reader_review_data = csv.reader(input_f)

    pn_wago_dic={} # 極性評価辞書 (キー:評価語、value:n/p)  
    pn_noun_dic={} #名詞活用語辞書 (キー:評価語、value:vp)
    
    # 入力：日本語評価極性辞書(用語編) 
    with open("./dic/wago.121808.pn",'r') as f:
        for pn_wago in f.readlines():
            pn_wago_tmp = pn_wago.split('\t')

            pn = pn_wago_tmp[0].split('（')[0]
            pn_text = pn_wago_tmp[1].replace(" ","").replace('\n','')

            # 極性評価辞書作成
            if pn == "ポジ":
                pn_wago_dic[pn_text] = 1
            elif pn == "ネガ":
                pn_wago_dic[pn_text] = -1

    # 入力：日本語評価極性辞書(名詞編)    
    with open("./dic/pn.csv.m3.120408.trim",'r') as f:
        for pn_noun in f.readlines():
            dic_value ={}
            pn_noun_tmp = pn_noun.split('\t')

            # 極性評価辞書作成
            if pn_noun_tmp[1] == "p" or pn_noun_tmp[1] == "n":
                 # 日本語評価極性辞書(名詞編)の中身：ネガポジ
                if pn_noun_tmp[1] == "p":
                    dic_value["pn"] = 1
                else:
                    dic_value["pn"] = -1

                # 日本語評価極性辞書(名詞編)の中身：活用語
                vps = pn_noun_tmp[2].split('（')[0].split('・')
                vp = [v.replace("〜", "") for v in vps]            
                dic_value["vp"] = vp

                pn_noun_dic[pn_noun_tmp[0]] = dic_value

    # 出力：レビューごとの係り受け結果
    file_name = "./data/output/result_pn" + str(datetime.datetime.today()) + ".csv"
    output_f = open(file_name, 'w')
    writer = csv.writer(output_f, lineterminator='\n')
    writer.writerow(["id","pn_word","bnst_left","bnst_right","text"])

    
    # レビューデータ分析
    for i,review_data in enumerate(Reader_review_data):

        print(i+1)        
        review_text=re.split(',',review_data[0])

        for text in review_text:
            
            # 係り受け解析(評価語チェックも並行)
            chunk_dic,pn_ids = run_cabocha.save_chunk(text,pn_wago_dic,pn_noun_dic)
            if chunk_dic == -1: # 評価語がない場合、スキップする
                continue
                
            # 文節ごとに、係り先順を取得
            chunk_order_dic = run_cabocha.get_chunk_order(chunk_dic)

            # 評価語 : 係り受け情報を取得
            for pn_id in pn_ids:

                # 係り受け情報(左)
                chunk_left = run_cabocha.get_chunk_left(chunk_dic,chunk_order_dic,pn_id)
                                                
                # 係り受け情報(右)
                chunk_right = run_cabocha.get_chunk_right(chunk_dic,chunk_order_dic,pn_id)
                                
                writer.writerow([i+1,chunk_dic[pn_id]["chunk_word"],chunk_left,chunk_right,text])
            

    input_f.close()
    output_f.close()

   
