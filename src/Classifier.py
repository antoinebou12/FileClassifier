#!/usr/bin/env python
"""
This script is a file classifier that organizes files in a directory based on their file type (audio, image, video, document, etc.).
It uses the Typer library to create a command-line interface for users to interact with the script.

"""

import os
import subprocess
import sys
from typing import List, Optional
from rich.console import Console
import typer
import arrow

from src import TopicModeler

app = typer.Typer()

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
        """
        def __init__(self, path: str, config: Optional[str] = None):
            self.get_config()
            self.path = path
            self.config = config
            self.topics = ['audio', 'image', 'video', 'archive', 'document', 'executable', 'font', 'web', 'config']
            self.topic_modeler = TopicModeler(
                num_topics=len(self.topics)
            )
            self.audio_formats = ['mp3', 'wav', 'wma', 'aac', 'flac', 'm4a', 'ogg', 'opus']
            self.image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'tiff']
            self.video_formats = ['mp4', 'mov', 'wmv', 'avi', 'avchd', 'flv', 'f4v', 'swf', 'mkv', 'webm', 'vob', 'ogv', 'drc', 'gifv', 'mng', 'mts', 'm2ts', 'ts', 'mxf', 'roq', 'nsv', 'amv', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm2v', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'f4p', 'f4a', 'f4b']
            self.archive_formats = ['zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'lz', 'lzma', 'tlz', 'txz', 'tzo', 'tar.lzma', 'tar.xz', 'tar.bz2', 'tbz2', 'tbz', 'tar.gz', 'tgz', 'Z', 'tar.Z', 'rar', 'zipx', 'iso', 'cab', 'dmg', 'cpio', 'cbr', 'cbz', 'cb7', 'cba', 'apk', 'jar', 'xar', 'pkg', 'deb', 'rpm']
            self.document_formats = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'odt', 'ods', 'odp', 'odg', 'odf', 'txt', 'rtf', 'tex', 'wks', 'wps', 'wpd', 'pages', 'numbers', 'key', 'csv']
            self.executable_formats = ['exe', 'msi', 'bin', 'apk', 'app', 'bat', 'cgi', 'com', 'gadget', 'jar', 'wsf']
            self.font_formats = ['ttf', 'otf', 'woff', 'woff2']
            self.web_formats = ['html', 'htm', 'css', 'js', 'php', 'json', 'xml']
            self.config_formats = ['conf', 'ini', 'cfg', 'cnf', 'config', 'properties', 'prop', 'settings', 'option', 'desktop', 'plist', 'reg', 'regedit', 'reged', 'regbak', 'regtrans-ms', 'cfg', 'conf', 'ini', 'properties', 'prop', 'desktop', 'plist', 'reg', 'regedit', 'reged', 'regbak', 'regtrans-ms']
            self.linux_formats = ['deb', 'rpm']
            self.windows_formats = ['exe', 'msi']
            self.mac_formats = ['dmg']
            self.books_formats = ['mobi', 'epub', 'chm']
            self.ignore_formats = ['part', 'desktop']
            self.console = Console()

        def get_config(self):
            if PLATFORM == 'darwin':
                self.config = os.path.join(os.path.expanduser('~'), '.classifier-master.conf')
            elif PLATFORM == 'win32' or OS == 'nt':
                self.config = os.path.join(os.getenv('userprofile'), 'classifier-master.conf')
            elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
                self.config = os.path.join(os.getenv('HOME'), '.classifier-master.conf')
            else:
                self.config = os.path.join(os.getcwd(), '.classifier-master.conf')

        def create_default_config(self):
                with open(self.config, "w") as conffile:
                    conffile.write("IGNORE: part, desktop\n" +
                    "Music: mp3, aac, flac, ogg, wma, m4a, aiff, wav, amr\n" +
                    "Videos: flv, ogv, avi, mp4, mpg, mpeg, 3gp, mkv, ts, webm, vob, wmv\n" +
                    "Pictures: png, jpeg, gif, jpg, bmp, svg, webp, psd, tiff\n" +
                    "Archives: rar, zip, 7z, gz, bz2, tar, dmg, tgz, xz, iso, cpio\n" +
                    "Documents: txt, pdf, doc, docx, odf, xls, xlsv, xlsx, " +
                    "ppt, pptx, ppsx, odp, odt, ods, md, json, csv\n" +
                    "Books: mobi, epub, chm\n" +
                    "DEBPackages: deb\n" +
                    "Programs: exe, msi\n" +
                    "RPMPackages: rpm")
                self.console.print(f"CONFIG file created at: {self.config}")
                return

        def check_config(self):
            """ create a default config if not available """
            if not os.path.isdir(os.path.dirname(self.config)):
                os.makedirs(os.path.dirname(self.config))
            if not os.path.isfile(self.config):
                self.create_default_config()

            with open(self.config, 'r') as file:
                for items in file:
                    spl = items.replace('\n', '').split(':')
                    key = spl[0].replace(" ","")
                    val = spl[1].replace(" ","")
                    self.formats[key] = val
            return

        def move_to(self, filename, from_folder, to_folder):
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
                # sourcery skip: low-code-quality
                for file in os.listdir(directory):
                        tmpbreak = False
                                # set up a config per folder
                        if file != DIRCONFFILE and os.path.isfile(
                            os.path.join(directory, file)):
                                filename, file_ext = os.path.splitext(file)
                                file_ext = file_ext.lower().replace('.', '')
                                if 'IGNORE' in self.formats:
                                    for ignored in self.formats['IGNORE'].replace('\n', '').split(','):
                                        if file_ext == ignored:
                                            tmpbreak = True
                                if not tmpbreak:
                                        for folder, ext_list in list(formats.items()):
                                                                    # never move files in the ignore list
                                                if folder != 'IGNORE':
                                                        folder = os.path.join(output, folder)
                                                        # make sure we are passing a list to the extension checker
                                                        if type(ext_list) == str:
                                                            ext_list = ext_list.split(',')
                                                        for tmp_ext in ext_list:
                                                                if file_ext == tmp_ext:
                                                                        try:
                                                                                self.moveto(file, directory, folder)
                                                                        except Exception as e:
                                                                                self.console.print(f'Cannot move file - {file} - {str(e)}')
                        """
                elif os.path.isdir(os.path.join(directory, file)) and self.args.recursive:
                    self.classify(self.formats, output, os.path.join(directory, file))
                """
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

        def classify_by_date(self, date_format, output, directory):
            self.console.print("Scanning Files")

            files = [x for x in os.listdir(directory) if not x.startswith('.')]
            creation_dates = map(lambda x: (x, arrow.get(os.path.getctime(os.path.join(directory, x)))), files)
            self.console.print(creation_dates)

            for file, creation_date in creation_dates:
                folder = creation_date.format(date_format)
                folder = os.path.join(output, folder)
                self.moveto(file, directory, folder)

            return

        def _format_text_arg(self, arg):
            """ Set a date format to name your folders"""
            if not isinstance(arg, str):
                arg = arg.decode('utf-8')
            return arg

        def _format_arg(self, arg):
            if isinstance(arg, str):
                arg = self._format_text_arg(arg)
            return arg

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Classify files in a directory"
)
@app.command()
def main(
    version: bool = typer.Option(False, "--version", help="Show version, filename and exit"),
    types: bool = typer.Option(False, "--types", help="Show the current list of types and formats"),
    edittypes: bool = typer.Option(False, "--edittypes", help="Edit the list of types and formats"),
    reset: bool = typer.Option(False, "--reset", help="Reset the default Config file"),
    specific_types: Optional[List[str]] = typer.Option(None, "--specific-types", help="Move all file extensions, given in the args list, in the current directory into the Specific Folder"),
    specific_folder: Optional[str] = typer.Option(None, "--specific-folder", help="Folder to move Specific File Type"),
    output: Optional[str] = typer.Option(None, "--output", help="Main directory to put organized folders"),
    directory: Optional[str] = typer.Option(None, "--directory", help="The directory whose files to classify"),
    date: bool = typer.Option(False, "--date", help="Organize files by creation date"),
    dateformat: Optional[str] = typer.Option(None, "--dateformat", help="Set the date format using YYYY, MM or DD"),
    topicmodel: bool = typer.Option(False, "--topicmodel", help="Perform topic modeling on text files"),
    extensions: Optional[str] = typer.Option(None, "--extensions", help="File extensions to consider for topic modeling (comma-separated)")
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
            extensions = classifier.args["extensions"].split(',')
        else:
            extensions = ['txt', 'pdf', 'doc', 'docx']  # Default extensions for topic modeling

        classifier.topic_modeling(classifier.args["directory"], extensions)
    classifier.run()

if __name__ == "__main__":
    app()