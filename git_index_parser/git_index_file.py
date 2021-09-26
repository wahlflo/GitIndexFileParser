from .git_index_file_entry import GitIndexFileEntry
from .git_index_file_extension import GitIndexFileExtension
from typing import List


class GitIndexFile:
    def __init__(self, version: int):
        self.version = version
        self.sha1 = None
        self._entries = list()
        self._extensions = list()

    def add_entry(self, entry: GitIndexFileEntry):
        self._entries.append(entry)

    def add_extensions(self, extension: GitIndexFileExtension):
        self._extensions.append(extension)

    def get_entries(self) -> List[GitIndexFileEntry]:
        return self._entries

    def get_extensions(self) -> List[GitIndexFileExtension]:
        return self._extensions