import pytest
import os
from src.Classifier import Classifier
from typer.testing import CliRunner

runner = CliRunner()

@pytest.fixture
def classifier():
    return Classifier(path="test_input")

def test_move_to(classifier):
    # Create temporary folders and a file to move
    os.makedirs("test_source")
    os.makedirs("test_destination")
    with open("test_source/test_file.txt", "w") as file:
        file.write("Test content")

    # Call the move_to function
    classifier.move_to("test_file.txt", "test_source", "test_destination")

    # Check if the file has been moved
    assert not os.path.exists("test_source/test_file.txt")
    assert os.path.exists("test_destination/test_file.txt")

    # Clean up temporary folders and files
    os.remove("test_destination/test_file.txt")
    os.rmdir("test_source")
    os.rmdir("test_destination")

def test_classify(classifier):
    # Create temporary folders and files
    os.makedirs("test_input", exist_ok=True)
    os.makedirs("test_output", exist_ok=True)
    with open("test_input/test_file.txt", "w") as file:
        file.write("Test content")

    # Call the classify function
    classifier.classify(classifier.formats, "test_output", "test_input")

    # Check if the file has been classified
    assert not os.path.exists("test_input/test_file.txt")
    assert os.path.exists("test_output/document/test_file.txt")

    # Clean up temporary folders and files
    os.remove("test_output/document/test_file.txt")
    os.rmdir("test_output/document")
    os.rmdir("test_output")
    os.rmdir("test_input")

if __name__ == '__main__':
    pytest.main()
