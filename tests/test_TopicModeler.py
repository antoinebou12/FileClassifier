import os
import pytest
from src.TopicModeler import TopicModeler

@pytest.fixture
def modeler():
    return TopicModeler(
        num_topics=5
    )

def test_lda_model(modeler):
    # Define a simple corpus with 2 topics
    corpus = [
        "The cat is on the mat.",
        "The dog is in the yard.",
        "The cat chases a mouse.",
        "The dog barks at the cat.",
        "The cat sleeps in the sun.",
        "The dog plays with a ball."
    ]

    # Save the corpus to test_input directory
    os.makedirs("test_input", exist_ok=True)
    for idx, document in enumerate(corpus):
        with open(f"test_input/doc_{idx}.txt", "w") as f:
            f.write(document)

    # Define the expected topics
    expected_topics = ["cat", "dog"]

    # Run the LDA model
    topics = modeler.topic_modeling(directory="test_input", extensions=["txt"], num_topics=2)

    print(topics)

    # Check if the identified topics match the expected topics
    for topic in topics:
        assert any(expected_word in topic for expected_word in expected_topics)

    # Clean up the test_input directory
    for file in os.listdir("test_input"):
        os.remove(os.path.join("test_input", file))
    os.rmdir("test_input")

if __name__ == '__main__':
    pytest.main()
