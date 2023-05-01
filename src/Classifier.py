#!/usr/bin/env python
"""
This script is a file classifier that organizes files in a directory based on their file type (audio, image, video, document, etc.).
It uses the Typer library to create a command-line interface for users to interact with the script.

"""

import os
import subprocess
import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
import arrow
import mimetypes

from src.TopicModeler import TopicModeler

VERSION = 'FileClassifier'
DIRCONFFILE = '.classifier.conf'
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
        formats = {
            "audio": ['mp3', 'wav', 'wma', 'aac', 'flac', 'm4a', 'ogg', 'opus'],
            "image": ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'tiff'],
            "video": ['mp4', 'mov', 'wmv', 'avi', 'avchd', 'flv', 'f4v', 'swf', 'mkv', 'webm', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'mts', 'm2ts', 'ts', 'mxf', 'roq', 'nsv', 'amv', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm2v', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'f4p', 'f4a', 'f4b'],
            "archive": ['7z', 'arj', 'deb', 'pkg', 'rar', 'rpm', 'tar.gz', 'z', 'zip'],
            "document": ['doc', 'docx', 'odt', 'pdf', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'txt', 'rtf'],
            "executable": ['apk', 'bat', 'bin', 'cgi', 'pl', 'com', 'exe', 'gadget', 'jar', 'msi', 'py', 'wsf'],
            "font": ['fnt', 'fon', 'otf', 'ttf'],
            "web": ['asp', 'aspx', 'cer', 'cfm', 'cgi', 'pl', 'css', 'htm', 'html', 'js', 'jsp', 'part', 'php', 'py', 'rss', 'xhtml'],
            "config": ['cfg', 'conf', 'ini', 'log', 'reg', 'url'],
            "database": ['accdb', 'db', 'dbf', 'mdb', 'pdb', 'sql'],
            "email": ['email', 'eml', 'emlx', 'msg', 'oft', 'ost', 'pst', 'vcf'],
            "presentation": ['key', 'odp', 'pps', 'ppt', 'pptx'],
            "programming": ['c', 'class', 'cpp', 'cs', 'h', 'java', 'sh', 'swift', 'vb'],
            "spreadsheet": ['ods', 'xls', 'xlsm', 'xlsx'],
            "system": ['bak', 'cab', 'cfg', 'cpl', 'cur', 'dll', 'dmp', 'drv', 'icns', 'ico', 'ini', 'lnk', 'msi', 'sys', 'tmp'],
            "misc": ['ics', 'ms', 'part', 'torrent'],
            "desktop": ['desktop', 'lnk'],
            "ignore": ['part', 'desktop'],
            "raw": ['raw'],
        }

        def __init__(self, path: str, config: Optional[str] = None):
            self.config = config
            self.get_config()
            self.path = path
            self.console = Console()

        def get_config(self):
            """Determines the appropriate configuration file location based on the platform."""
            if PLATFORM == 'darwin':
                self.config = os.path.join(
                    os.path.expanduser('~'), '.classifier-master.conf')
            elif PLATFORM == 'win32' or OS == 'nt':
                self.config = os.path.join(
                    os.getenv('userprofile'), 'classifier-master.conf')
            elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
                self.config = os.path.join(
                    os.getenv('HOME'), '.classifier-master.conf')
            else:
                self.config = os.path.join(
                    os.getcwd(), '.classifier-master.conf')

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

            with open(self.config, 'r') as file:
                for items in file:
                    if items.strip() and ":" in items:
                        key, val = items.strip().split(':')
                        key = key.strip()
                        val = val.strip().split(', ')
                        self.formats[key] = val
            return

        def check_minetypes(self):
            for category, extensions in self.formats.items():
                self.console.print(f"{category.upper()}:")
                for extension in extensions:
                    mimetype, _ = mimetypes.guess_type(f"file.{extension}")
                    self.console.print(f"  - {extension}: {mimetype}")
                self.console.print()

        def move_to(self, filename, from_folder, to_folder):
            """
            Moves a file from the source folder to the destination folder.

            Args:
                filename (str): The name of the file to move.
                from_folder (str): The path of the source folder containing the file.
                to_folder (str): The path of the destination folder to move the file to.
            """
            from_file = os.path.join(from_folder, filename)
            to_file = os.path.join(to_folder, filename)
                # to move only files, not folders
            if to_file != from_file:
                    self.console.print(f'moved: {str(to_file)}')
                    if os.path.isfile(from_file):
                        if not os.path.exists(to_folder):
                            os.makedirs(to_folder)
                        os.rename(from_file, to_file)
            return

        def classify(self, formats, output, directory):
            """
            Classifies and moves the files in the specified directory based on their file type.
            """
            for file in os.listdir(directory):
                if file != DIRCONFFILE and os.path.isfile(os.path.join(directory, file)):
                    filename, file_ext = os.path.splitext(file)
                    file_ext = file_ext.lower().replace('.', '')

                    if not self._should_ignore(file_ext):
                        dest_folder = self._get_destination_folder(file_ext, formats, output)
                        if dest_folder is not None:
                            try:
                                self.move_to(file, directory, dest_folder)
                            except Exception as e:
                                self.console.print(f'Cannot move file - {file} - {str(e)}')
                                continue
            return

        def classify_by_date(self, date_format, output, directory):
                creation_dates = self._init_classify_by_date(directory)
                for file, creation_date in creation_dates:
                    folder = creation_date.format(date_format)
                    folder = os.path.join(output, folder)
                    self.move_to(file, directory, folder)

                return

        def classify_by_date_range(self, date_format, output, directory, start_date, end_date):
                creation_dates = self._init_classify_by_date(directory)
                for file, creation_date in creation_dates:
                    if start_date <= creation_date <= end_date:
                        folder = creation_date.format(date_format)
                        folder = os.path.join(output, folder)
                        self.move_to(file, directory, folder)

                return

        def _init_classify_by_date(self, directory):
                self.console.print("Scanning Files")
                files = [x for x in os.listdir(directory) if not x.startswith('.')]
                result = map(
                    lambda x: (
                        x,
                        arrow.get(os.path.getctime(os.path.join(directory, x))),
                    ),
                    files,
                )
                self.console.print(result)
                return result

        def classify_by_topic_modeling(self, output, directory):
            self.console.print("Scanning Files")

            files = [x for x in os.listdir(directory) if not x.startswith('.')]
            for file in files:
                folder = self.topic_modeling(file)
                folder = os.path.join(output, folder)
                self.move_to(file, directory, folder)

            return

        def open_editor(self):
            match PLATFORM:
                case 'darwin':
                    subprocess.call(('open', '-t', self.config))
                case 'win32' | 'nt':
                    os.startfile(self.config)
                case 'linux' | 'linux2' | 'posix':
                    subprocess.Popen(['xdg-open', self.config])
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
            if 'IGNORE' in self.formats:
                for ignored in self.formats['IGNORE'].replace('\n', '').split(','):
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
                if folder != 'IGNORE':
                    folder = os.path.join(output, folder)
                    if type(ext_list) == str:
                        ext_list = ext_list.split(',')
                    for tmp_ext in ext_list:
                        if file_ext == tmp_ext:
                            return folder
            return None

        def _format_text_arg(self, arg):
            """ Set a date format to name your folders"""
            if not isinstance(arg, str):
                arg = arg.decode('utf-8')
            return arg

        def _format_arg(self, arg):
            if isinstance(arg, str):
                arg = self._format_text_arg(arg)
            return arg