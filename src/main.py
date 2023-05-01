from typing import List
from typing import Optional

import typer

from src import Classifier


app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Classify files in a directory",
)
@app.command()
def main(
    version: bool = typer.Option(
        False, "--version", help="Show version, filename and exit"
    ),
    types: bool = typer.Option(
        False, "--types", help="Show the current list of types and formats"
    ),
    edittypes: bool = typer.Option(
        False, "--edittypes", help="Edit the list of types and formats"
    ),
    reset: bool = typer.Option(False, "--reset", help="Reset the default Config file"),
    specific_types: Optional[List[str]] = typer.Option(
        None,
        "--specific-types",
        help="Move all file extensions, given in the args list, in the current directory into the Specific Folder",
    ),
    specific_folder: Optional[str] = typer.Option(
        None, "--specific-folder", help="Folder to move Specific File Type"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", help="Main directory to put organized folders"
    ),
    directory: Optional[str] = typer.Option(
        None, "--directory", help="The directory whose files to classify"
    ),
    date: bool = typer.Option(False, "--date", help="Organize files by creation date"),
    dateformat: Optional[str] = typer.Option(
        None, "--dateformat", help="Set the date format using YYYY, MM or DD"
    ),
    topicmodel: bool = typer.Option(
        False, "--topicmodel", help="Perform topic modeling on text files"
    ),
    extensions: Optional[str] = typer.Option(
        None,
        "--extensions",
        help="File extensions to consider for topic modeling (comma-separated)",
    ),
):
    classifier = Classifier()
    classifier.args = {
        "version": version,
        "types": types,
        "edittypes": edittypes,
        "reset": reset,
        "specific_types": specific_types,
        "specific_folder": specific_folder,
        "output": output,
        "directory": directory,
        "date": date,
        "dateformat": dateformat,
        "topicmodel": topicmodel,
        "extensions": extensions,
    }

    if classifier.args["topicmodel"]:
        if classifier.args["extensions"]:
            extensions = classifier.args["extensions"].split(",")
        else:
            extensions = [
                "txt",
                "pdf",
                "doc",
                "docx",
            ]  # Default extensions for topic modeling

        classifier.topic_modeling(classifier.args["directory"], extensions)
    classifier.run()


if __name__ == "__main__":
    app()
