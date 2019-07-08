import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import numpy as np
from scipy import spatial
from config import get_config


config = get_config()


class Similarity:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.vocab_ids = [x for x in self.nlp.vocab.vectors.keys()]
        self.vocab_vectors = [self.nlp.vocab.vectors[x] for x in self.vocab_ids]
        self.vocab_vectors = np.array(self.vocab_vectors)

    def __filter_by_pos_tag(self, doc, pos_tags, stop_words, lemmatize=True):
        words = []
        for sent in doc.sents:
            for token in sent:
                if token.pos_ in pos_tags and token.text not in stop_words:
                    words.append(token.lemma_ if lemmatize else token.text)
        return list(set(words))

    def __words_2_vector(self, words):
        words = np.array([self.nlp(word).vector for word in words])
        vector = np.mean(words, axis=0)

        return vector

    def get_vector(self, text, candidate_pos_tags=None):
        if not candidate_pos_tags:
            candidate_pos_tags = config.SIMILARITY_POS_TAGS

        doc = self.nlp(text)
        words = self.__filter_by_pos_tag(doc=doc,
                                         pos_tags=candidate_pos_tags,
                                         stop_words=STOP_WORDS)
        if words:
            return self.__words_2_vector(words=words)

        return None

    def similarity(self, source, vectors):
        scores = spatial.distance.cdist(np.array([source]), vectors, metric=config.SIMILARITY_METRIC)
        return scores

    def __vector_2_word(self, vector, num=2):
        output_word = []
        closest_ids = spatial.distance.cdist(np.array([vector]), self.vocab_vectors, metric=config.SIMILARITY_METRIC).argsort()[0]
        for idx in closest_ids:
            if len(output_word) >= num:
                break

            word_id = self.vocab_ids[idx]
            word = self.nlp.vocab[word_id].text
            word = self.nlp(word)[0].lemma_.lower()

            if word not in output_word:
                output_word.append(word)
        return output_word

    def get_keywords(self, text, num=2):
        vector = self.get_vector(text=text)
        return self.__vector_2_word(vector=vector, num=num)


if __name__ == '__main__':
    s = Similarity()
    out = s.get_keywords(text="If you're a successful guy and you have a lot of money, you have to have a lot of women in your life. It's not a choice or a choice of who you sleep with. It's a choice of who you sleep with.",
                         num=2)
    print(out)


