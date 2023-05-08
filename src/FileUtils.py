import mimetypes
import os

from rich.tree import Tree


class FileUtils:
    formats = {
        "audio": ["mp3", "wav", "wma", "aac", "flac", "m4a", "ogg", "opus", "aiff", "mid", "amr"],
        "image": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "tiff"],
        "video": [
            "mp4",
            "mov",
            "wmv",
            "avi",
            "avchd",
            "flv",
            "f4v",
            "swf",
            "mkv",
            "webm",
            "vob",
            "ogv",
            "drc",
            "gifv",
            "mng",
            "mts",
            "m2ts",
            "ts",
            "mxf",
            "roq",
            "nsv",
            "amv",
            "m4p",
            "m4v",
            "mpg",
            "mp2",
            "mpeg",
            "mpe",
            "mpv",
            "m2v",
            "m4v",
            "svi",
            "3gp",
            "3g2",
            "mxf",
            "roq",
            "nsv",
            "f4p",
            "f4a",
            "f4b",
        ],
        "archive": ["7z", "arj", "deb", "pkg", "rar", "rpm", "tar.gz", "z", "zip"],
        "document": [
            "doc",
            "docx",
            "odt",
            "pdf",
            "xls",
            "xlsx",
            "ods",
            "ppt",
            "pptx",
            "txt",
            "rtf",
            "tex",
            "wpd",
            "csv",
            "tsv",
            "md",
            "odp",
            "pages",
        ],
        "executable": [
            "apk",
            "bat",
            "bin",
            "cgi",
            "pl",
            "com",
            "exe",
            "gadget",
            "jar",
            "msi",
            "py",
            "wsf",
        ],
        "font": ["fnt", "fon", "otf", "ttf", "woff", "woff2", "eot"],
        "web": [
            "asp",
            "aspx",
            "cer",
            "cfm",
            "cgi",
            "pl",
            "css",
            "htm",
            "html",
            "js",
            "jsp",
            "part",
            "php",
            "py",
            "rss",
            "xhtml",
            "xul",
            "crdownload",
        ],
        "config": ["cfg", "conf", "ini", "log", "reg", "url"],
        "database": ["accdb", "db", "dbf", "mdb", "pdb", "sql"],
        "email": ["email", "eml", "emlx", "msg", "oft", "ost", "pst", "vcf"],
        "presentation": ["key", "odp", "pps", "ppt", "pptx"],
        "programming": ["c", "class", "cpp", "cs", "h", "java", "sh", "swift", "vb"],
        "spreadsheet": ["ods", "xls", "xlsm", "xlsx"],
        "system": [
            "bak",
            "cab",
            "cfg",
            "cpl",
            "cur",
            "dll",
            "dmp",
            "drv",
            "icns",
            "ico",
            "ini",
            "lnk",
            "msi",
            "sys",
            "tmp",
        ],
        "application": ["p7m", "p7s", "xpi", "p8", "wmf", "trm"],
        "misc": ["ics", "ms", "part", "torrent"],
        "desktop": ["desktop", "lnk"],
        "ignore": ["part", "desktop"],
        "raw": ["raw"],
        "data": ["dat"],
        "shortcut": ["lnk"],
        "config": ["cfg", "conf", "ini", "log", "reg", "url"],
        "torrent": ["torrent"],
        "vector": ["svg", "ai", "eps", "ps"],
        "3d": ["3ds", "obj", "fbx", "blend", "stl", "ply"],
        "adobe": ["psd", "xd", "ai", "eps", "ps"],
        "cad": ["dwg", "dxf"],
        "gis": ["shp", "kml", "kmz"],
        "raster": ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "gif"],
    }

    folders = {
        "windows": ["$RECYCLE.BIN", "System Volume Information"],
        "linux": [".Trash-1000", ".Trash-1001", ".Trash-1002", ".Trash-1003"],
        "mac": [".Trashes"],
        "ignore": ["$RECYCLE.BIN", "System Volume Information", ".Trashes"],
        "git": [".git"],
        "venv": ["venv"],
        "node": ["node_modules"],
        "python": ["__pycache__"],
        "java": ["target"],
        "c": ["Debug", "Release"],
        "c++": ["Debug", "Release"],
        "c#": ["Debug", "Release"],
        "go": ["bin", "pkg"],
        "rust": ["target"],
        "php": ["vendor"],
        "ruby": ["bin"],
        "kotlin": ["out"],
        "scala": ["target"],
        "swift": ["build"],
        "typescript": ["node_modules"],
        "javascript": ["node_modules"],
        "dart": ["build"],
        "haskell": ["dist"],
        "julia": ["bin"],
        "test": ["test"],
        "jetbrains": ["out", ".idea"],
        "vscode": [".vscode"],
        "sublime": [".sublime-project", ".sublime-workspace"],
        "vim": [".vim", ".viminfo", ".backup", ".swp"],
        "emacs": [".emacs.d"],
        "atom": [".atom"],
        "jupyter": [".ipynb_checkpoints"],
    }

    def __init__(self, path, config, console):
        self.path = path
        self.config = config
        self.console = console

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
            self.console.print(f"moved: {str(to_file)}")
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
                self.print_tree(os.path.join(root, dir), level=level - 1, parent=child)

        self.console.print(tree)

    def exists(self, filename):
        return os.path.exists(filename)

    def check_copy_name(self, filename, directory):
        # check if the file with a name with (1) or de words copy already exists
        if os.path.exists(os.path.join(directory, filename)):
            filename = self.get_file_name(filename)
            filename = filename.replace("(1)", "")
            filename = filename.replace("copy", "")
            filename = filename.strip()
            filename = f"{filename}(1){self.get_file_extension(filename)}"

        return filename

    def check_if_git_repo(self, directory):
        return os.path.exists(os.path.join(directory, ".git"))

    def percentage_of_formats(self, directory):
        formats = {}
        for file in os.listdir(directory):
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower().replace(".", "")
            if file_ext in formats:
                formats[file_ext] += 1
            else:
                formats[file_ext] = 1
        return formats

    def percentage_of_file_types(self, directory):
        file_types = {}
        for file in os.listdir(directory):
            file_type = self.get_file_type(file)
            if file_type in file_types:
                file_types[file_type] += 1
            else:
                file_types[file_type] = 1
        return file_types

    def percentage_of_folder_types(self, directory):
        folder_types = {}
        for root, dirs, files in os.walk(directory):
            for _ in dirs:
                folder_type = self.folders
                if folder_type in folder_types:
                    folder_types[folder_type] += 1
                else:
                    folder_types[folder_type] = 1