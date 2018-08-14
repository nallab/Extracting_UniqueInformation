#!/usr/bin/env python3A
# -*- coding: utf-8 -*-

import CaboCha

"""
レビュー文の構文解析結果を保存

in:
 「レビュー文」「評価語辞書」
out:
 評価語があれば、「構文解析結果の辞書」「評価語idリスト」
 評価語がなければ、「-1」
"""
def save_chunk(text,pn_wago_dic,pn_noun_dic):  

    pn_flag = False
    pn_id = []
    chunk_dic ={}
    
    c = CaboCha.Parser()
    tree = c.parse(text)

    for i in range(tree.chunk_size()):
        
        dic_value ={}
        
        # 文節(chunk)情報
        chunk = tree.chunk(i)
        chunk_id = i
        chunk_link = chunk.link

        # 形態素(token)情報
        chunk_word = ""
        pos_list = []
        token_start = chunk.token_pos
        token_end = chunk.token_pos + chunk.token_size
        
        for j  in range(token_start,token_end):
            token = tree.token(j)
            features = token.feature.split(',') # 要素
            normalized_surface = token.normalized_surface # 表層
            pos = features[0] # 品詞
            
            # 評価語フラグ (名詞)
            if normalized_surface in pn_noun_dic:
                # 評価語(名詞)が文末か否か
                if chunk.link == -1: # 評価語(名詞)が文末のとき、利用する                    
                    pn_flag = True
                    pn_id.append(i)
                    
                else: # 評価語(名詞)が文末で無いとき、 係り先の動詞を確認  
                    chunkp = tree.chunk(chunk.link)
                    for p_j in range(chunkp.token_pos, chunkp.token_pos + chunkp.token_size):
                        tokenp = tree.token(p_j)
                        for vp in pn_noun_dic[normalized_surface]["vp"]:
                            if vp == tokenp.feature.split(',')[6]:
                                pn_flag = True
                                pn_id.append(i)
                                
            # 評価語フラグ (用言)
            if normalized_surface in pn_wago_dic:
                pn_flag = True
                pn_id.append(i)
                                
                    
            # 形態素を文節単位に結合
            chunk_word += normalized_surface

            # 形態素ごとの品詞をリストに追加
            pos_list.append(pos)
            

            # 辞書追加
            dic_value["chunk_link"] = chunk.link
            dic_value["chunk_word"] = chunk_word
            dic_value["chunk_pos"] = pos_list
            
            chunk_dic[chunk_id] = dic_value

    # 評価語チェッカー
    if pn_flag:
        return chunk_dic,pn_id
    else:
        return -1,-1

"""
係り受け関係のid順を取得する

in：構文解析結果の辞書 
out:係り受け関係のid順

"""
def get_chunk_order(chunk_dic):
    chunk_order_dic = {}

    # 1. 全ての文節の係り受け順(id)を取得する
    for my_id in chunk_dic.keys():

        flag = True
        my_list=[my_id]
        serch_id = my_id

        # 1-1. 文節ごとに、最後の係り先になるまでループする
        while flag:
            chunk_link = chunk_dic[serch_id]["chunk_link"]

            if chunk_link != -1: # 係り先が最後じゃないとき、係り先のidを格納
                my_list.append(chunk_dic[serch_id]["chunk_link"])
                
            else: # 係り先が最後のとき、ループを抜ける
                flag = False
                
            serch_id = chunk_link # 1-2.係り先のidを次の探索idとする
            
        chunk_order_dic[my_id]  = my_list # 1-3.文節ごとに、係り受け順を格納
    
    return chunk_order_dic


"""
最後の係り元idを取得する

in：構文解析結果の辞書
out:最後の係り元idを取得     

"""
def get_chunk_end(chunk_dic):
    
    end_list = []

    # 1. 文節ごとに、他の文節の親になっているか調べる
    for my_id in chunk_dic.keys():

        # 1-1. 他の文節の親を調査
        for value in chunk_dic.values():
            
            if my_id == value["chunk_link"]: # 文節の親になっている場合、false
                flag = False
                break
            else: # 文節の親になっていない場合、true
                flag = True

        if flag:
            end_list.append(my_id) # リストに追加する
            
    return end_list

"""
ターゲット単語の左側のidを取得する

in：構文解析結果の辞書、係り受け関係のid順、ターゲットid
out:ターゲット単語の左側のid (複数あり)

"""
def get_chunk_left(chunk_dic,chunk_order_dic,keyword_id):
    
    chunk_left = []
    end_list = get_chunk_end(chunk_dic)
    pos_flag = False

    # 1. 係り受けルートにターゲット単語あったとき、左側の単語を取得
    for i in end_list:
        serch_list = chunk_order_dic[i]

        # 1-2. 係り受けルートにターゲット単語があるか調べる
        if keyword_id in serch_list:
            pos_flag = False            
            p = serch_list.index(keyword_id)

            if p != 0: # 評価語が係り受けidが0になることはないため
                tmp_list = []
                
                # 1-3. ターゲット単語の左側の単語を取得
                for j in range(p):
                    
                    left_id = serch_list[j]
                    
                    if "名詞" in chunk_dic[left_id]["chunk_pos"]: # 係り元のチャンクに名詞がある場合
                        pos_flag = True
                        tmp_list.append(chunk_dic[left_id]["chunk_word"])

            #1-4. 取得したものをリストに格納
            if pos_flag:
                del chunk_left
                chunk_left = tmp_list
                
    return chunk_left

    

"""
ターゲット単語の右側のidを取得する
in：係り受け関係のid順、ターゲットid
out:ターゲット単語の右側のid (1つのみ)
"""
def get_chunk_right(chunk_dic,chunk_order_dic,keyword_id):

    chunk_right = []
    # 1. 係り関係順を元に、ターゲットの右側単語を取得
    for right_id in chunk_order_dic[keyword_id]:
        if right_id != keyword_id:
            if "名詞" in chunk_dic[right_id]["chunk_pos"]: # 係り先のチャンクに名詞がある場合
                chunk_right.append(chunk_dic[right_id]["chunk_word"])

    return chunk_right
    
