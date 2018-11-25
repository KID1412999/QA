#从文本获取rdf数据
import ast
import fool
import LtpExtract
def subject(txt):#抽取句子主语
    s=fool.analysis([i.split('，') for i in txt.split('。')][0][0])[1][0][0]
    if s[2]=='person' or s[2]=='org' or s[2]=='company' or s[2]=='location':
        return s[3]
def add_ude(txt):#分句词组之间增加“的”
    s=[]
    if '的' not in txt:
        j=fool.analysis(txt)[1][0]
        #print(j)
        for i in j:
            s.append([i[3],i[2]])
    for i in s:
        if i[1]=='job':
            txt=txt.replace(i[0],i[0]+'是')
        elif i[1]=='company' or i[1]=='person' or i[1]=='org':
            txt=txt.replace(i[0],i[0]+'的')
    if txt[-1]=='是' or txt[-1]=='的':
        txt=txt[:-1]
    return txt
def clearup(txt):#去掉形容词
    s=[]
    k=fool.analysis(txt)[0][0]
    if debug:
        print(k)
    for i in range(len(k)):
        if k[i][1]=='d' and k[i+1][1]=='a' and k[i+2][1]=='ude':
            s.append(k[i][0]+k[i+1][0]+k[i+2][0])
        elif k[i][1]=='a' and k[i+1][1]=='ude':
            s.append(k[i][0]+k[i+1][0])
        elif k[i][1]=='a' and k[i+1][1]!='ude':
            s.append(k[i][0])
        elif k[i][1]=='d':
            s.append(k[i][0])
    for i in s:
        txt=txt.replace(i,'')
    return txt
def extract_knowledge(article):#抽取知识
    knowledge=[]
    for j in [i.replace('。','').replace('、','，') for i in article.split('。')]:
        try:
            knowledge.append(justy(j))
        except Exception:
            pass
    return knowledge
def justy(txt):
    s=[]
    global l,debug,subj
    txt=clearup(txt)#去掉形容词
    if '，' in txt:
        sents=txt.split('，')
        if debug:
            print(subj)
            print('处理的分句',sents)
        for i in sents:
            i=i.replace('它',subj).replace('他',subj).replace('她',subj)#处理指示代词
            if debug:
                print('---->>',i)
            st=LtpExtract.extract(i)
            if debug:
                print('第一次分析',i,st)
            if st :
                s.append(st)
         
            else:
                if debug:
                    print('---->>',subj+i)
                st=LtpExtract.extract(subj+i)
                if st:
                    s.append(st)
             
                else:
                    if debug:
                        print('---->>',subj+'是'+i)
                    st=LtpExtract.extract(subj+'是'+i)
                    if st:
                        s.append(st)
                    
                    else:
                        if debug:
                            print('---->>',subj+add_ude(i))
                        st=LtpExtract.extract(subj+add_ude(i))
                        if st:
                            s.append(st)
                          
        
    
    return s
