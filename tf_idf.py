import jieba

from collections import Counter




# bow = Counter()
# bow.update(a)



'''Parameters:
** Document : {no.: [splitting words]}
** total_D : total amount of documents
** N : times of how many document including specific word
'''

add_word = ['同', '黃金', '後者', '源於', '慾望', '為了', '綻放']
for w in add_word:
    jieba.add_word(w)   

test_sent = (
"有兩個人非常渴，喝同一口井水時，一個用黃金杯，一個用陶土杯\n"
"前者覺得自己富貴，後者認為自己貧賤；前者得到虛榮滿足，後者陷入無謂煩惱\n"
"他們都忘了，自己需要的是水，而不是盛水的杯\n"
"生活亦如此，快樂源於知足，煩惱生自慾望\n"
"活得是否快樂幸福，取決於心態，而不是虛榮和不必要的佔有\n"
"花開，不是為了花落，而是為了綻放；生命，不是為了抱怨，而是為了成長\n"
)




s = [" ".join(jieba.cut(test_sent))]

whole_bow = Counter()
single_bow

for word in s[0].split(" "):
    whole_bow.update([word])
print(whole_bow)




'''
Document = {}
word_Dict = {}

i = 0
for sent in test_sent:
    print(i, sent)
    i += 1





def computeTF(wordDict, bow):
    
    # wordDict: {word : count}
    
    tfDict = {}
    bowCount = len(bow)

    for word, count in wordDict.items():
        
    
    return tfDict
'''
