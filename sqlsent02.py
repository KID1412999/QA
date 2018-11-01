# coding: utf-8
#语法分析
import nltk
import jieba.posseg as pseg
import jieba
import ast
import fool
from nltk import CFG

def product_grammar(s):#根据词性构造语法
    l=fool.analysis(s)[0][0]
    k={}
    y=[]
    print(l)
    for i in l:
        if i[1] not in y:
            y.append(i[1])
            k.update({i[1]:[i[0]]})
        else:
            k.update({i[1]:k[i[1]]+[i[0]]})
    g=''
    for i,j in k.items():
        t=i+' ->'
        c=0
        for n in j:
            if len(j)>1 and c<=len(j)-2:
                t+='\''+n+'\''+'|'
            else:
                t+='\''+n+'\''
            c+=1
        g+=t+'\n'
    print('文法:',g)
    return g

def draw_1(s):
    m=s
    l=fool.cut(s)[0]
    print(l)
    p=product_grammar(m)
    grammar = CFG.fromstring("""
    S ->NP V NP U L|NP U NP V L| NP U L V NP|L U NP V NP|L V NP U NP|NP V L U NP
    NP -> N N|r NP|NP A NP|M Q NP|N|NP U NP|A U NP|N NP|NP C NP|NP U|M NP
    VP ->V|V NP|V VP|A VP|VP NP|VP U|VP C VP|VP P|VP uguo
    V -> v|vi|vshi
    N ->n|nr|t|ns|f|nx|nz
    R ->r
    C ->c
    P ->p
    L ->R|R NP
    U ->ude|y
    A ->a|d|ad
    M ->m
    Q ->q
    """+p)
    cp= nltk.ChartParser(grammar)
    tree=cp.parse(l)
    stree=[]
    for s in tree:
        st=[]
        #s.draw()
        for i in range(len(s)):
            st.append([s[i].label(),''.join(s[i].leaves())])
        stree.append(st)
    return stree
def sqlsent(text):
    st=draw_1(text)
    print(st[0])
    t=st[0]
    l=t
    if t[1][0]=='V' and t[-1][0]=='L':
        l=t[2:]+[t[1]]+[t[0]]
    elif t[1][0]=='V' and t[0][0]=='L':
        l=t[2:]+[t[1]]+[t[0]]
    elif t[1][0]=='V' and t[2][0]=='L':
        l=t[2:]+[t[1]]+[t[0]]

    de=[]
    for i in l:
        if i[0]=='L':
            de.append('L')
        elif i[0]=='NP':
            de.append(i[1])
    return de

if __name__=='__main__':
    print(sqlsent('谁是马云的儿子'))

