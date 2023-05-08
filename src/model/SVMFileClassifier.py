import os
import re

import pandas as pd
from sklearn import svm
from sklearn.base import accuracy_score
from sklearn.calibration import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


class SVMFileClassifier:
    def __init__(self, features=None, kernel="linear", C=1.0):
        if features is None:
            features = ["extension"]
        self.features = features
        self.kernel = kernel
        self.C = C
        self.vectorizer = CountVectorizer()
        self.label_encoder = LabelEncoder()
        self.classifier = svm.SVC(kernel=self.kernel, C=self.C)

    def extract_course(self, text):
        pattern = re.compile(r"(course|class|subject):\s*([^\n]+)", re.IGNORECASE)
        return match.group(2) if (match := pattern.search(text)) else ""

    def preprocess(self, text):
        return self.extract_course(text)

    def load_files(self, directory, extensions):
        files = []
        for file in os.listdir(directory):
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace(".", "")

            if file_ext in extensions and os.path.isfile(os.path.join(directory, file)):
                with open(
                    os.path.join(directory, file),
                    encoding="utf-8",
                    errors="ignore",
                ) as f:
                    text = f.read()
                    files.append({"text": text, "extension": file_ext})
        return pd.DataFrame(files)

    def fit(self, X, y):
        self.vectorizer.fit(X)
        X_vec = self.vectorizer.transform(X)
        self.label_encoder.fit(y)
        y_enc = self.label_encoder.transform(y)
        self.classifier.fit(X_vec, y_enc)

    def predict(self, X):
        X_vec = self.vectorizer.transform(X)
        y_enc = self.classifier.predict(X_vec)
        return self.label_encoder.inverse_transform(y_enc)

    def evaluate(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.fit(X_train, y_train)
        y_pred = self.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        print(f"Accuracy: {acc}")
        print(f"Classification report:\n{report}")


def run_topic_modeling():
    # Create an instance of the SVMFileClassifier class
    classifier = SVMFileClassifier(
        features=["extension", "course"], kernel="linear", C=1.0
    )

    # Load files into a pandas dataframe
    df = classifier.load_files("file_directory", ["pdf", "docx"])

    # Preprocess the data and split into X and y
    df["course"] = df["text"].apply(classifier.preprocess)
    X = df[["extension", "course"]].values
    y = df["extension"].values

    # Fit the classifier on the input data
    classifier.fit(X, y)

    # Make predictions on new data
    X_new = [["pdf", "CSE 101"], ["docx", "CSE 101"]], [
        ["pdf", "CSE 101"],
        ["docx", "CSE 101"],
    ]
    y_pred = classifier.predict(X_new)
    print(y_pred)

    classifier.evaluate(X, y)
