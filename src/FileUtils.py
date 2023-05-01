

import os
import mimetypes
from rich.tree import Tree


class FileUtils(object):

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

    def __init__(self, path, config, console):
        self.path = path
        self.config = config
        self.console = console

    def load_documents(self, directory, extensions):
        documents = []
        for file in os.listdir(directory):
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace('.', '')

            if file_ext in extensions and os.path.isfile(os.path.join(directory, file)):
                with open(os.path.join(directory, file), 'r', encoding='utf-8', errors='ignore') as f:
                    documents.append(f.read())
        return documents

    def move_to_directory(self, source, destination):
        os.makedirs(destination, exist_ok=True)
        for file in os.listdir(source):
            os.rename(os.path.join(source, file), os.path.join(destination, file))
        os.rmdir(source)

    def remove_directory(self, directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)

    def check_minetypes(self):
            for category, extensions in self.file_utility.formats.items():
                self.console.print(f"{category.upper()}:")
                for extension in extensions:
                    mimetype, _ = mimetypes.guess_type(f"file.{extension}")
                    self.console.print(f"  - {extension}: {mimetype}")
                self.console.print()

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

    def get_file_type(self, filename):
        file_type = mimetypes.guess_type(filename)[0]
        file_type = "unknown" if file_type is None else file_type.split("/")[0]
        return file_type

    def get_file_extension(self, filename):
        return os.path.splitext(filename)[1]

    def get_file_name(self, filename):
        return os.path.splitext(filename)[0]

    def get_file_size(self, filename):
        return os.path.getsize(filename)

    def get_file_path(self, filename):
        return os.path.abspath(filename)

    def list_files(self, directory):
        return os.listdir(directory)

    def list_files_recursive_with_path(self, directory, level=3):
        files = []
        for root, dirs, files in os.walk(directory):
            level -= 1
            if level < 0:
                break
            for file in files:
                files.append(os.path.join(root, file))
        return files

    def print_tree(self, directory, level=3):
        tree = Tree(directory)

        for root, dirs, files in os.walk(directory):
            if level < 1:
                break
            level -= 1

            root_dir = tree.get_node(root)

            for file in files:
                root_dir.add(file)

            for dir in dirs:
                child = root_dir.add(dir)
                self.print_tree(os.path.join(root, dir), level=level-1, parent=child)

        self.console.print(tree)