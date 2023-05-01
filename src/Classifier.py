#!/usr/bin/env python
"""
This script is a file classifier that organizes files in a directory based on their file type (audio, image, video, document, etc.).
It uses the Typer library to create a command-line interface for users to interact with the script.

"""
import os
import subprocess
import sys
from typing import Optional

import arrow
from rich.console import Console

from src.FileUtils import FileUtils
from src.model.TopicModeler import TopicModeler

VERSION = "FileClassifier"
DIRCONFFILE = ".classifier.conf"
PLATFORM = sys.platform
OS = os.name


class Classifier:
    """
    All format lists were taken from wikipedia, not all of them were added due to extensions
    not being exclusive to one format such as webm, or raw
    Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
    Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
    Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
    Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
    Minetypes 	-	https://www.freeformatter.com/mime-types-list.html
    """

    def __init__(self, path: str, config: Optional[str] = None):
        self.config = config
        self.get_config()
        self.path = path
        self.console = Console()
        self.file_utils = FileUtils(self.path, self.config, self.console)
        self.topic_modeler = TopicModeler()

    def get_config(self):
        """Determines the appropriate configuration file location based on the platform."""
        if PLATFORM == "darwin":
            self.config = os.path.join(
                os.path.expanduser("~"), ".classifier-master.conf"
            )
        elif PLATFORM == "win32" or OS == "nt":
            self.config = os.path.join(
                os.getenv("userprofile"), "classifier-master.conf"
            )
        elif PLATFORM == "linux" or PLATFORM == "linux2" or OS == "posix":
            self.config = os.path.join(os.getenv("HOME"), ".classifier-master.conf")
        else:
            self.config = os.path.join(os.getcwd(), ".classifier-master.conf")

    def create_default_config(self):
        """Creates a default configuration file if one is not available."""

        with open(self.config, "w") as conffile:
            conffile.write("IGNORE: part, desktop\n")
            for category, extensions in self.formats.items():
                conffile.write(f"{category.capitalize()}: {', '.join(extensions)}\n")

        self.console.print(f"CONFIG file created at: {self.config}")
        return

    def check_config(self):
        """Checks for the existence of the configuration file and reads it into the `formats` dictionary."""
        if not os.path.isdir(os.path.dirname(self.config)):
            os.makedirs(os.path.dirname(self.config))
        if not os.path.isfile(self.config):
            self.create_default_config()

        with open(self.config) as file:
            for items in file:
                if items.strip() and ":" in items:
                    key, val = items.strip().split(":")
                    key = key.strip()
                    val = val.strip().split(", ")
                    self.file_utility.formats[key] = val
        return

    def move_to(self, filename, from_folder, to_folder):
        self.file_utility.move_to(filename, from_folder, to_folder)

    def classify(self, formats, output, directory):
        """
        Classifies and moves the files in the specified directory based on their file type.
        """
        for file in os.listdir(directory):
            if file != DIRCONFFILE and os.path.isfile(os.path.join(directory, file)):
                filename, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower().replace(".", "")

                if not self._should_ignore(file_ext):
                    dest_folder = self._get_destination_folder(
                        file_ext, formats, output
                    )
                    if dest_folder is not None:
                        try:
                            self.move_to(file, directory, dest_folder)
                        except Exception as e:
                            self.console.print(f"Cannot move file - {file} - {str(e)}")
                            continue
        return

    def classify_by_date(self, date_format, output, directory):
        creation_dates = self._init_classify_by_date(directory)
        for file, creation_date in creation_dates:
            folder = creation_date.format(date_format)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_date_range(
        self, date_format, output, directory, start_date, end_date
    ):
        creation_dates = self._init_classify_by_date(directory)
        for file, creation_date in creation_dates:
            if start_date <= creation_date <= end_date:
                folder = creation_date.format(date_format)
                folder = os.path.join(output, folder)
                self.move_to(file, directory, folder)

        return

    def _init_classify_by_date(self, directory):
        self.console.print("Scanning Files")
        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        result = map(
            lambda x: (
                x,
                arrow.get(os.path.getctime(os.path.join(directory, x))),
            ),
            files,
        )
        self.console.print(result)
        return result

    def classify_by_extension(self, output, directory):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace(".", "")
            folder = file_ext
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_size(self, output, directory, size):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.size(file, directory, size)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_size_range(self, output, directory, min_size, max_size):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.size_range(file, directory, min_size, max_size)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_author(self, output, directory):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.author(file, directory)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_most_recent(self, output, directory, number):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.most_recent(file, directory, number)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_oldest(self, output, directory, number):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.oldest(file, directory, number)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def classify_by_topic_modeling(self, output, directory):
        self.console.print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith(".")]
        for file in files:
            folder = self.topic_modeling(file)
            folder = os.path.join(output, folder)
            self.move_to(file, directory, folder)

        return

    def open_editor(self):
        match PLATFORM:
            case "darwin":
                subprocess.call(("open", "-t", self.config))
            case "win32" | "nt":
                os.startfile(self.config)
            case "linux" | "linux2" | "posix":
                subprocess.Popen(["xdg-open", self.config])
            case _:
                self.console.print("Unsupported platform.")
                return

    def _should_ignore(self, file_ext):
        """
        Determines whether a file extension should be ignored based on the 'IGNORE' list.

        Args:
            file_ext (str): The file extension to check.

        Returns:
            bool: True if the file extension should be ignored, False otherwise.
        """
        if "IGNORE" in self.file_utility.formats:
            for ignored in (
                self.file_utility.formats["IGNORE"].replace("\n", "").split(",")
            ):
                if file_ext == ignored:
                    return True
        return False

    def _get_destination_folder(self, file_ext, formats, output):
        """
        Determines the destination folder for a file based on its extension.

        Args:
            file_ext (str): The file extension to check.
            formats (dict): The dictionary of file formats and their corresponding folders.
            output (str): The output directory.

        Returns:
            str: The destination folder for the file.
        """
        for folder, ext_list in list(formats.items()):
            if folder != "IGNORE":
                folder = os.path.join(output, folder)
                if type(ext_list) == str:
                    ext_list = ext_list.split(",")
                for tmp_ext in ext_list:
                    if file_ext == tmp_ext:
                        return folder
        return None

    def _format_text_arg(self, arg):
        """Set a date format to name your folders"""
        if not isinstance(arg, str):
            arg = arg.decode("utf-8")
        return arg

    def _format_arg(self, arg):
        if isinstance(arg, str):
            arg = self._format_text_arg(arg)
        return arg
