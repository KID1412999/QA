#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-
import os
from pyltp import Postagger
from pyltp import Segmentor#分词
from pyltp import Postagger#词性标注
import fool
from pyltp import Parser
LTP_DATA_DIR = './ltp_data_v3.4.0'  # ltp模型目录的路径

pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型

par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

def segment(txt):#结合NER的分词
    ner=[i[3] for i in fool.analysis(txt)[1][0]]
    words=[]
    for i in ner:
        txt=txt.replace(i[0],'|||'+i[0]).replace(i[-1],i[-1]+'|||')
    txt=txt.split('|||')
    for i in txt:
        if i in ner:
            words.append(i)
        else:
            for j in fool.analysis(i)[0][0]:
                words.append(j[0])
    return words

def pos_tag(word):
    global postagger
    postags = postagger.postag(word)  # 词性标注
    # print (' '.join(postags))
    # print(word)
    #postagger.release()  # 释放模型
    return [i for i in postags]

def parser_sets(word,postags):
    global parser
    words = word
    postag= [ i for i in postags ]
    arcs = parser.parse(words, postag)  # 句法分析
    rely_id = [arc.head for arc in arcs]    # 提取依存父节点id
    relation = [arc.relation for arc in arcs]   # 提取依存关系
    heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语
    sets={}
    for i in range(len(words)):
        sets[relation[i]]=[ words[i] ,heads[i]]
        print (relation[i] + '(' + words[i] + ', ' + heads[i] + ')')
    #parser.release()  # 释放模型
    return deal(sets)

def deal(sets):
    rdfs=[]
    if 'SBV' in sets.keys() and 'ATT' in sets.keys():
        rdfs.append((sets['ATT'][0],sets['ATT'][1],sets['SBV'][0]))
        print(sets['ATT'][0],sets['ATT'][1],sets['SBV'][0])
    if 'SBV' in sets.keys() and 'VOB' in sets.keys():
        rdfs.append((sets['SBV'][0],sets['VOB'][1],sets['VOB'][0]))
        print(sets['SBV'][0],sets['VOB'][1],sets['VOB'][0])
    if 'ATT' in sets.keys() and 'VOB' in sets.keys():
        if sets['ATT'][1]!=sets['VOB'][0]:
            rdfs.append((sets['ATT'][0],sets['ATT'][1],sets['VOB'][0]))
            print(sets['ATT'][0],sets['ATT'][1],sets['VOB'][0])
    if 'SBV' in sets.keys() and 'POB' in sets.keys():
        if fool.analysis(sets['POB'][0])[1][0][0][2]!='time':
            rdfs.append((sets['SBV'][0],sets['SBV'][1],sets['POB'][0]))
            print(sets['SBV'][0],sets['SBV'][1],sets['POB'][0])
    return rdfs


def extract(text):
    words=segment(text)#分词
    postags=pos_tag(words)#词性标注
    return parser_sets(words,postags)#依存分析

if __name__=='__main__':
    text='罗永浩1972年出生于重庆市'
    extract(text)
