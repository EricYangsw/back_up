from __future__ import print_function, unicode_literals
import os
import sys


import jieba


# 增加詞
jieba.add_word('石墨烯')
jieba.add_word('凱特琳')

test_sent = (
"李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
"例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
"「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
)
words = jieba.cut(test_sent)
print('/'.join(words))





#Segmentation
print("="*40)
print("Try jieba.posseg")

import jieba.posseg as pseg
result = pseg.cut(test_sent)
for w in result:
    print(w.word, "/", w.flag, ",", end=' ')




#Segmentation
print("="*40)
print("Test frequency tune")

testlist = [
('今天天气不错', ('今天', '天气')),
('如果放到post中将出错。', ('中', '将')),
('我们中出了一个叛徒', ('中', '出')),
]

for sent, seg in testlist:
    print('/'.join(jieba.cut(sent, HMM=False)))
    word = ''.join(seg)
    print('%s Before: %s, After: %s' % (word, jieba.get_FREQ(word), jieba.suggest_freq(seg, True)))
    print('/'.join(jieba.cut(sent, HMM=False)))
    print("Next line"+"="*40)
# add_word(word, freq=None, tag=None) 和 del_word(word) 可在程序中动态修改词典。
# suggest_freq(segment, tune=True) 可调节单个词语的词频，使其能（或不能）被分出来。
#注意：自动计算的词频在使用 HMM 新词发现功能时可能无效。














'''
def read():
    fp = open('./nlp/word.txt', "r", encoding = 'utf8') # default= 'big5'
    content = fp.read()
    fp.close()
    return content
    
content = read()

jieba.set_dictionary('./nlp/token/dict.txt.big')
seg_list = jieba.cut(content, cut_all=False)
print("Default Model:", " ".join(seg_list))
'''



'''Loading dictionary: 
jieba.load_userdict(file_name)

format: 詞、詞頻（可省略）、詞性（可省略）
创新办 3 i
云计算 5
凱特琳 nz
台中
'''



print("fold path: " ,os.getcwd())
print(__name__, "Return: ", 0)






