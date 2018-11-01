import requests
from lxml import etree
import jieba
import jieba.posseg as psg

class AI:
	def __init__(self):
		print("Hello,我是智能问答机器人，给我一根网线，我就可以帮你找到一切问题的答案！")
		self.question=''
		self.text=''
	def ask(self,q):
		self.question=q
		print('你的问题是：',self.question)
		#print([(x.word,x.flag) for x in psg.cut(self.question)])
	def anwser(self):
		head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.3'}
		html=requests.get('https://www.baidu.com/s?wd='+self.question,headers=head)
		html.encoding='utf-8'
		ele=etree.HTML(html.text)
		s=ele.xpath("/html//h3/a//text()")
		abs=ele.xpath("/html//div[@class='c-abstract']/text()[2]")#获取摘要
		#print('答案是：')
		#print(abs[0],'--->')
		return abs
	def zhidao(self):
		head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.3'}
		html=requests.get('https://zhidao.baidu.com/search?word='+self.question,headers=head)
		html.encoding='gbk'
		ele=etree.HTML(html.text)
		s=ele.xpath('''/html//dl[@data-fb="pos:dt>a,type:normal"]//dd[1]''')
		self.text=[ ''.join(i.xpath('''.//text()''')) for i in s ]
if __name__=='__main__':
	a=AI()
	a.ask('笛卡尔是哪个国家的？')
	print(a.anwser())
