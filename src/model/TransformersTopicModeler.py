import os

from nltk.tokenize import word_tokenize
from transformers import pipeline


class TransformersTopicModeler:
    def __init__(self, model_name, num_topics=5):
        self.num_topics = num_topics
        self.model = pipeline("text2text-generation", model=model_name)

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalnum() and token not in self.stop_words
        ]
        return tokens

    def load_documents(self, directory, extensions):
        documents = []
        for file in os.listdir(directory):
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace(".", "")

            if file_ext in extensions and os.path.isfile(os.path.join(directory, file)):
                with open(
                    os.path.join(directory, file),
                    encoding="utf-8",
                    errors="ignore",
                ) as f:
                    documents.append(f.read())
        return documents

    def topic_modeling(self, directory, extensions, num_topics=5):
        documents = self.load_documents(directory, extensions)
        TransformersTopicModeler(num_topics)
        topics = []

        for document in documents:
            text = self.preprocess(document)
            generated_text = self.model(text, max_length=50, num_return_sequences=1)[0][
                "generated_text"
            ]
            topics.append(generated_text)

        return topics
