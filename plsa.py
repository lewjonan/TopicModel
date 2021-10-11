import random
import numpy as np
import prettytable

from utils import get_logger, norm


class PlsaModel:
    def __init__(self, data, number_of_topics, max_iters):
        self.data = data
        self.number_of_topics = number_of_topics
        self.max_iters = max_iters

        self.logger = get_logger("plsa")

        self.word_posterior_prob_on_topic = np.zeros((self.number_of_topics, self.data.vocabulary_size), dtype=np.float) # P(w|z)
        self.topic_posterior_prob_on_document = np.zeros((self.data.number_of_documents, self.number_of_topics), dtype=np.float) # P(z|d)
        self.topic_posterior_prob_on_word_document = np.zeros((self.data.number_of_documents, self.data.vocabulary_size, self.number_of_topics), dtype=np.float) # P(z)

        self.init_params()

    def init_params(self):
        self.word_posterior_prob_on_topic = np.random.random(self.word_posterior_prob_on_topic.shape)
        self.topic_posterior_prob_on_document = np.random.random(self.topic_posterior_prob_on_document.shape)
        self.topic_posterior_prob_on_word_document = np.random.random(self.topic_posterior_prob_on_word_document.shape)

    def show_result(self):
        self.logger.info("print some sample of restults...")

        show_doc_ids = np.random.choice(self.data.number_of_documents, 5)

        for doc_id in show_doc_ids:
            self.logger.info("text: " + self.data.documents[doc_id].text)
            cur_topic_prob = self.topic_posterior_prob_on_document[doc_id]

            topic_ids = np.argsort(-cur_topic_prob)[:5]
            for i, topic_id in enumerate(topic_ids):
                self.logger.info("topic %d prob %.4f" % (i, cur_topic_prob[topic_id]))

                cur_word_prob = self.word_posterior_prob_on_topic[topic_id]
                word_ids = np.argsort(-cur_word_prob)[:5]

                words = [self.data.vocabulary[word_id] for word_id in word_ids]
                word_probs = [self.word_posterior_prob_on_topic[topic_id, word_id] for word_id in word_ids]
                tb = prettytable.PrettyTable(words)
                tb.add_row(word_probs)
                self.logger.info("\n" + tb.get_string())


    def fit(self):
        for iter in range(self.max_iters):
            self.logger.info("run iteration %d" % iter)

            # E step
            for doc_id in range(self.data.number_of_documents):
                for word_id in range(self.data.vocabulary_size):
                    prob = self.word_posterior_prob_on_topic[:, word_id] * self.topic_posterior_prob_on_document[doc_id, :]
                    self.topic_posterior_prob_on_word_document[doc_id][word_id] = prob

            self.topic_posterior_prob_on_word_document = norm(self.topic_posterior_prob_on_word_document, dim=-1)

            # M step
            for topic_id in range(self.number_of_topics):
                for word_id in range(self.data.vocabulary_size):
                    p = 0
                    for doc_id in range(self.data.number_of_documents):
                        p += self.data.word_document_co_occurrence_matrix[word_id][doc_id] * self.topic_posterior_prob_on_word_document[doc_id, word_id, topic_id]
                    self.word_posterior_prob_on_topic[topic_id][word_id] = p

            self.word_posterior_prob_on_topic = norm(self.word_posterior_prob_on_topic, dim=-1)

            for topic_id in range(self.number_of_topics):
                for doc_id in range(self.data.number_of_documents):
                    p = 0
                    for word_id in range(self.data.vocabulary_size):
                        p += self.data.word_document_co_occurrence_matrix[word_id][doc_id] * self.topic_posterior_prob_on_word_document[doc_id, word_id, topic_id]
                    self.topic_posterior_prob_on_document[doc_id][topic_id] = p

            self.topic_posterior_prob_on_document = norm(self.topic_posterior_prob_on_document, dim=-1)
