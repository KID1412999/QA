# coding: utf-8
#句子相似度分析
from gensim.models import word2vec
from gensim.models import Word2Vec,KeyedVectors
import gensim
import jieba
import os
import numpy as np
from scipy.linalg import norm

model = KeyedVectors.load_word2vec_format("70000-small.txt")

def vector_similarity(s1, s2):
	def sentence_vector(s):
		words = jieba.lcut(s)
		v = np.zeros(200)
		for word in words:
			try:
				v += model[word]
			except:
				v +=np.random.uniform(-0.25,0.25,200)
		v /= len(words)
		return v
	v1, v2 = sentence_vector(s1), sentence_vector(s2)
	return np.dot(v1, v2) / (norm(v1) * norm(v2))
if __name__=='__main__':
	s1 = '马云的生日是1974年吗？'
	s2 = '马云是95年出生的'
	print(s1,s2,'相似度',vector_similarity(s1, s2))
