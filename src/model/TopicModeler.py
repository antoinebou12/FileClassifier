import os
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

class TopicModeler:
    def __init__(self, num_topics=5):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        self.num_topics = num_topics
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in self.stop_words]
        return tokens

    def fit_transform(self, documents):
        texts = [self.preprocess(document) for document in documents]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]

        return models.LdaModel(
            corpus, num_topics=self.num_topics, id2word=dictionary, passes=15
        )

    def load_documents(self, directory, extensions):
        documents = []
        for file in os.listdir(directory):
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace('.', '')

            if file_ext in extensions and os.path.isfile(os.path.join(directory, file)):
                with open(os.path.join(directory, file), 'r', encoding='utf-8', errors='ignore') as f:
                    documents.append(f.read())
        return documents

    def topic_modeling(self, directory, extensions, num_topics=5):
        documents = self.load_documents(directory, extensions)
        topic_modeler = TopicModeler(num_topics)
        lda = topic_modeler.fit_transform(documents)

        topics = []
        for i in range(lda.num_topics):
            topic = ', '.join([term for term, freq in lda.show_topic(i)])
            topics.append(topic)
        return topics