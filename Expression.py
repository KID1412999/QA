#数学表达式求值
import fool
def expression(sent):
    st=''
    sent=sent.replace('平方','**2').replace('减','-').replace('加','+').replace('乘','*').replace('除','/').replace('立方','**3')
    x=['w','wp']
    print(sent)
    print(analysis(sent)[0][0])
    for i in analysis(sent)[0][0]:
        if i[1] in x and i[0]!='=' or i[0].isdigit():
            st+=i[0]
    print('表达式',st)
    return eval(st)
if __name__=='main':
	expression('发的广泛地421+奋斗45乘以44等于多少啊？')
