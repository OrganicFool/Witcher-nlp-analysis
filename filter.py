import jieba
import re
import os
import codecs

# NOVEL=['Baptism of Fire','Defying the Times','Elven Blood','Lady of the Lake','Swallow Tower','Sword of Destiny','The Last Wishes']


def removePunctuation(text):
    punctuation = '!,;:?"\'？。！【】；、{}：“”’‘|《》，/…＊．'
    text = re.sub(r'[{}]+'.format(punctuation),'',text)
    return text.strip()

def preprocess():
    jieba.enable_paddle()

    with codecs.open("corpus.txt",'w','utf-8') as standard:
        for novel in os.listdir('resources/'):
            path='resources/'+novel
            print("novel " + novel + " start loading")

            with open(path,'r',encoding='utf-8') as f:
                str=f.read()
                sentences = re.split("(。|！|\!|\.|？|\?)", str)
                new_sents = []

                for i in range(int(len(sentences) / 2)):
                    sent = sentences[2 * i] + sentences[2 * i + 1]
                    new_sents.append(removePunctuation(sent))

                for sent in new_sents:
                    if sent != '':
                        split_sent=' '.join(jieba.cut(sent,use_paddle=True))
                        standard.write(split_sent+'\n')
            print("novel "+novel+" finished")

if __name__ == '__main__':
    preprocess()





