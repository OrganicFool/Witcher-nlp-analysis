import jieba
import re
import os
import codecs

names = ['杰洛特','叶奈法','希里','恩希尔','雷吉斯','弗尔泰斯特','卡兰瑟','特莉丝','邦哈特','菲丽芭','密尔瓦','丹德里恩','卓尔坦']


def remove_punctuation(text):
    # punctuation = '!,;:?"\'？。！【】；、{}：“”’‘|《》，/…＊．「」—-）（'
    text = re.sub("[^0-9A-Za-z\u4e00-\u9fa5]", '', text)
    return text.strip()


def entity_mapping(texts):
    return list(map(word_mapping, texts))


def word_mapping(word):
    entity_dict = {'猎魔士': '猎魔人', '叶妮芙': '叶奈法', '雷恩斯': '雷吉斯', '厄维尔': '科维尔',
                   '特丽斯': '特莉丝', '雷吉思': '雷吉斯', '亚斯克尔': '丹德里恩', '丹德莱恩': '丹德里恩',
                   '希里雅': '希里', '茜瑞': '希里', '茜瑞菈': '希里', '琴特拉': '辛特拉'}

    if word in entity_dict:
        return entity_dict[word]
    else:
        return word


def preprocess_regardless_stopwords():
    jieba.enable_paddle()
    for name in names:
        jieba.suggest_freq(name, tune=True)

    with codecs.open("corpus.txt", 'w', 'utf-8') as standard:
        standard.seek(0)
        standard.truncate()

        for novel in os.listdir('resources/'):
            path = 'resources/'+novel
            print("novel " + novel + " start loading")

            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                sentences = re.split("(。|！|\!|\.|？|\?)", text)
                print("there are " + str(len(sentences)) + " sentences in this novel")

                new_sents = []

                for i in range(int(len(sentences) / 2)):
                    sent = sentences[2 * i] + sentences[2 * i + 1]
                    new_sents.append(remove_punctuation(sent))

                for sent in new_sents:
                    if sent != '':
                        split_sent = ' '.join(entity_mapping(jieba.cut(sent, use_paddle=True)))
                        standard.write(split_sent+'\n')
            print("novel "+novel+" finished")


def preprocess_with_stopwords():
    print("started to filter and split corpus with stop words")
    jieba.enable_paddle()
    for name in names:
        jieba.suggest_freq(name, tune=True)

    print("started to loading stop words dictionary")
    stop_words = {'的'}
    with open('stopwords.txt', encoding='utf-8') as f:
        while True:
            stop_word = f.readline()
            if stop_word == '':
                break

            stop_word = stop_word.strip()
            stop_words.add(stop_word)
    print("stop words dictionary has been loaded")

    for name in stop_words:
        jieba.suggest_freq(name, tune=True)

    with codecs.open("corpus_without_stopword.txt", 'w', 'utf-8') as standard:
        standard.seek(0)
        standard.truncate()

        for novel in os.listdir('resources/'):
            path = 'resources/'+novel
            print("novel " + novel + " start loading")

            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                sentences = re.split("(。|！|\!|\.|？|\?)", text)
                print("there are " + str(len(sentences)) + " sentences in this novel")

                new_sents = []
                for i in range(int(len(sentences) / 2)):
                    sent = sentences[2 * i] + sentences[2 * i + 1]
                    new_sents.append(remove_punctuation(sent))

                for sent in new_sents:
                    if sent != '':
                        split_sentence = jieba.cut(sent, use_paddle=True)
                        out_sentence = ''
                        for word in split_sentence:
                            if word not in stop_words:
                                out_sentence += word_mapping(word)
                                out_sentence += ' '
                        standard.write(out_sentence+'\n')
            print("novel "+novel+" finished")


if __name__ == '__main__':
    preprocess_regardless_stopwords()
    preprocess_with_stopwords()
