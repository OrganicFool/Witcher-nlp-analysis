from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from  gensim import corpora
import pandas as pd

corpus="coupus.txt"


def process():
    sentences = LineSentence('corpus.txt')
    w2v_model=Word2Vec(sentences,size=100,window=5, min_count=3, workers=4)
    vocabulary=w2v_model.wv.vocab
    w2v_model.save("model.model")
    w2v_dict = {}
    for word in vocabulary:
        w2v_dict.update({word: w2v_model[word]})
    x = pd.DataFrame(w2v_dict)
    x.to_csv("vec.csv", index=0)


if __name__ == '__main__':
    process()
