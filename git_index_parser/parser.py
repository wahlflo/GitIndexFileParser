import binascii
import collections
import struct
from .git_index_file_extension import GitIndexFileExtension
from .git_index_file_entry import GitIndexFileEntry
from .git_index_file import GitIndexFile
import io


class GitIndexParserException(Exception):
    def __init__(self, message: str):
        self.message = message


class GitIndexParser:
    @staticmethod
    def check(boolean: bool, message: str):
        if not boolean:
            raise GitIndexParserException(message=message)

    @staticmethod
    def parse_file(path_to_file) -> GitIndexFile:
        content = io.BytesIO(open(path_to_file, mode='rb').read())
        return GitIndexParser.parse(file=content)

    @staticmethod
    def parse(file: io.BytesIO) -> GitIndexFile:
        try:
            return GitIndexParser._parse(file=file)
        except GitIndexParserException as exception:
            raise exception
        except Exception as exception:
            raise GitIndexParserException(message=str(exception))

    @staticmethod
    def _parse(file: io.BytesIO) -> GitIndexFile:

        def read(read_format):
            # "All binary numbers are in network byte order."
            # Hence "!" = network order, big endian
            read_format = "! " + read_format
            read_bytes = file.read(struct.calcsize(read_format))
            return struct.unpack(read_format, read_bytes)[0]

        # 4-byte signature, b"DIRC"
        index_signature = file.read(4).decode("ascii")
        GitIndexParser.check(index_signature == "DIRC", "Not a Git index file")

        # 4-byte version number
        index_version = read("I")
        GitIndexParser.check(index_version in {2, 3}, "Unsupported version: {}".format(index_version))

        # 32-bit number of index entries, i.e. 4-byte
        number_of_entries = read("I")
        parsed_index_file = GitIndexFile(version=index_version)

        for n in range(number_of_entries):

            entry_ctime_seconds = read("I")
            entry_ctime_nanoseconds = read("I")

            entry_mtime_seconds = read("I")
            entry_mtime_nanoseconds = read("I")

            entry_dev = read("I")
            entry_ino = read("I")

            # 4-bit object type, 3-bit unused, 9-bit unix permission
            entry_mode = read("I")

            entry_uid = read("I")
            entry_gid = read("I")
            entry_size = read("I")

            entry_sha1 = binascii.hexlify(file.read(20)).decode("ascii")
            entry_flags = read("H")

            # 1-bit extended, must be 0 in version 2
            entry_extended = bool(entry_flags & (0b01000000 << 8))

            # 12-bit name length, if the length is less than 0xFFF (else, 0xFFF)
            name_length = entry_flags & 0xFFF

            # 62 bytes so far
            entry_length = 62

            if entry_extended and (parsed_index_file.version == 3):
                entry_extra_flags = read("H")
                # 13-bits unused
                entry_length += 2
            else:
                entry_extra_flags = None

            if name_length < 0xFFF:
                entry_name = file.read(name_length).decode("utf-8", "replace")
                entry_length += name_length
            else:
                name = []
                while True:
                    byte = file.read(1)
                    if byte == "\x00":
                        break
                    name.append(byte)
                entry_name = b''.join(name).decode("utf-8", "replace")
                entry_length += 1

            pad_length = (8 - (entry_length % 8)) or 8
            nulls = file.read(pad_length)
            GitIndexParser.check(set(nulls) == {0}, "padding contained non-NUL")

            entry = GitIndexFileEntry(index=n + 1, name=entry_name,
                                      ctime_seconds=entry_ctime_seconds, ctime_nanoseconds=entry_ctime_nanoseconds,
                                      mtime_seconds=entry_mtime_seconds, mtime_nanoseconds=entry_mtime_nanoseconds,
                                      dev=entry_dev, ino=entry_ino, mode=entry_mode, uid=entry_uid, gid=entry_gid, size=entry_size,
                                      flags=entry_flags, extra_flags=entry_extra_flags, sha1=entry_sha1)
            parsed_index_file.add_entry(entry=entry)

        index_length = file.getbuffer().nbytes
        extension_number = 1

        while file.tell() < (index_length - 20):
            extension = collections.OrderedDict()
            extension["extension"] = extension_number
            extension_signature = file.read(4).decode("ascii")
            extension_size = read("I")

            extension_data = file.read(extension_size)
            extension_data = extension_data.decode("iso-8859-1")

            extension = GitIndexFileExtension(extension_number=extension_number, signature=extension_signature, size=extension_size, data=extension_data)
            parsed_index_file.add_extensions(extension=extension)
            extension_number += 1

        parsed_index_file.sha1 = binascii.hexlify(file.read(20)).decode("ascii")

        file.close()
        return parsed_index_file
