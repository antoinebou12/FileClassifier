import pytest
from classifier import TopicModeler

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

    # Define the expected topics
    expected_topics = ["cat", "dog"]

    # Run the LDA model
    topics = modeler.lda_model(corpus, num_topics=2)

    # Check if the identified topics match the expected topics
    for topic in topics:
        assert any(expected_word in topic for expected_word in expected_topics)


if __name__ == '__main__':
    pytest.main()
