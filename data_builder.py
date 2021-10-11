import re
import glob
import jieba
import numpy as np

from utils import get_logger


class Document:
    def __init__(self, fp, stopwords):
        self.fp = fp
        self.stopwords = stopwords
        self.text = None
        self.clean_text = None
        self.words = []

        self._preprocess()

    def _load_data(self):
        with open(self.fp, "r", encoding="utf-8") as f:
            text = f.read()

        return text

    def _clean_text(self, text):
        pattern = re.compile(r"[^\u4e00-\u9fa5]+")
        clean_text = re.sub(pattern, "", text)

        return clean_text

    def _tokenize(self, text):
        word_generator = jieba.cut(text, cut_all=False)
        word_list = [word for word in word_generator]

        return word_list

    def _preprocess(self):
        self.text = self._load_data()
        self.clean_text = self._clean_text(self.text)
        self.words = self._tokenize(self.clean_text)

        self.words = [word for word in self.words if word not in self.stopwords]


class Corpus:
    def __init__(self, data_dir, stopwords):
        self.logger = get_logger("data")

        self.logger.info("load data...")

        self.documents = []
        for fp in glob.glob(data_dir)[:100]:

            self.documents.append(Document(fp, stopwords))

        self.number_of_documents = len(self.documents)

        self._build_vocabulary()
        self._build_word_document_co_occurrence_matrix()

        self.logger.info("vocabulary size: %d" % self.vocabulary_size)
        self.logger.info("number of documents: %d" % self.number_of_documents)

    def _build_vocabulary(self):
        unique_set = set()
        for document in self.documents:
            for word in document.words:
                unique_set.add(word)

        self.vocabulary = list(unique_set)
        self.vocabulary_size = len(self.vocabulary)

    def _build_word_document_co_occurrence_matrix(self):
        self.word_document_co_occurrence_matrix = np.zeros((self.vocabulary_size, len(self.documents)), dtype=np.long)
        for doc_id, document in enumerate(self.documents):
            for word in document.words:
                word_id = self.vocabulary.index(word)
                self.word_document_co_occurrence_matrix[word_id][doc_id] += 1


            