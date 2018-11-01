import requests
from lxml import etree
import rdflib
import sqlsent02
import SentAna
import fool
# 与RDF的交互
from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, retract_fact, load
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
prefix0 = "http://www.example.org/" # URI的统一前缀
abbr = lambda x: x[len(prefix0):]                  # 取URI的缩写，为了展示的简洁
verbose = lambda x: prefix0+x                      # 恢复缩写为URI的全称
vbose=lambda x:('<'+verbose(x)+'>') if x!='?x' else x
datas=[]
pyDatalog.create_terms('X,Y,R,relation')

def add_data(e1,r,e2,g):
    r=rdflib.URIRef(verbose(r))
    e1=rdflib.URIRef(verbose(e1))
    e2=rdflib.URIRef(verbose(e2))
    g.add((e1,r,e2))
    #g.serialize("graph.rdf")
    
def search(name):
    url='https://baike.baidu.com/item/'+name
    html=requests.get(url,headers=head)
    html.encoding='utf-8'
    text=html.text
    ele=etree.HTML(text)
    t1=[ ''.join(i.xpath('.//text()')).replace('\n','').replace('\xa0','').replace(' ','') for i in ele.xpath('/html//dd[@class="basicInfo-item value"]')]
    t2=[ ''.join(i.xpath('.//text()')).replace('\xa0','').replace('\n','').replace(' ','') for i in ele.xpath('/html//dt[@class="basicInfo-item name"]')]
    return list(zip(t2,t1))
    
def query(text):
    global datas
    for i in fool.analysis(text)[1]:
        for j in i:
            for i in search(j[3]):
                add_data(j[3],i[0],i[1],g)
    ss=sqlsent02.sqlsent(text)
    #print(ss,'???')
    for i in ss:
        if '的' in i:
            ss[ss.index(i)]=query(i+'是什么')
    #print(ss,'--')
    ss[ss.index('L')]='?x'
    q = "select ?x where { "+vbose(ss[0])+" ?x ?y}"
    x = g.query(q)
    t=0
    st=''
    for i in list(x):
        simi=SentAna.vector_similarity(abbr(i[0]),ss[1])
        if simi>=t:
            st=abbr(i[0])
            t=simi
    ss[1]=st
    #逻辑推导
    for subj, pred, obj in g:        #从RDF取出三元组
        assert_fact("relation",abbr(subj),abbr(pred), abbr(obj))     #加入Datalog数据库
    load("relation(X,'爷爷',Z) <= relation(X,'父亲',Y) & relation(Y,'父亲',Z)")#定义推理表达式
    load("relation(Y,'孙子',X) <= relation(X,'爷爷',Y)")
    load("relation(Y,'丈夫',X) <= relation(X,'妻子',Y)")
    load("relation(Y,'儿子',X) <= relation(X,'父亲',Y)")
    load("relation(Y,'奶奶',Z) <= relation(Y,'爷爷',X)& relation(X,'配偶',Z)")
    load("relation(X,'儿媳',Z) <= relation(X,'孙子',Y)& relation(Y,'母亲',Z)")
    load("relation(X,'亲属',Y) <= relation(X,'孙子',Y)")
    load("relation(X,'亲属',Y) <= relation(X,'母亲',Y)")
    load("relation(X,'亲属',Y) <= relation(X,'奶奶',Y)")
    load("relation(X,'亲属',Y) <= relation(X,'儿子',Y)")
    load("relation(X,'亲属',Y) <= relation(X,'爷爷',Y)")
    load("relation(X,'亲属',Y) <= relation(X,'父亲',Y)")
    load("relation(X,'亲属',Y) <= relation(Y,'亲属',X)")
    for i in relation(X,R,Y):
        add_data(i[0],i[1],i[2],g)
    q = "select ?x where { "+vbose(ss[0])+' '+vbose(ss[1])+' '+vbose(ss[2])+"}"
    x = g.query(q)
    datas=[ abbr(i[0]) for i in x]
    return abbr(list(x)[0][0])
    
g = rdflib.Graph()
#读取
g.parse("someFile.ttl", format="turtle")
query('王思聪的亲属是谁')
print(datas)
#存储为Turtle格式
str0 =g.serialize(format='turtle')
open("someFile.ttl","wb").write(str0)
