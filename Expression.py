#数学表达式求值
import fool
def expression(sent):
	st=''
	sent=sent.replace('加上','+').replace('减去','-').replace('乘以','*').replace('除以','/')\
.replace('加','+').replace('减','-').replace('乘','*').replace('除','/')\
.replace('的平方','**2')
	x=['w','m','wp']
	for i in fool.analysis(sent)[0][0]:
		if i[1] in x and i[0]!='=':
			st+=i[0]
	print('表达式',st)
	return eval(st)
if __name__=='main':
	expression('发的广泛地421+奋斗45乘以44等于多少啊？')
