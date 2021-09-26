

class GitIndexFileEntry:
    def __init__(self, index: int, name: str, ctime_seconds: int, ctime_nanoseconds: int, mtime_seconds: int, mtime_nanoseconds: int, dev: int, ino: int, mode: int, uid: int,
                 gid: int, size: int, flags, extra_flags, sha1: str):
        self.index = index
        self.name = name
        self.ctime_seconds = ctime_seconds
        self.ctime_nanoseconds = ctime_nanoseconds
        self.mtime_seconds = mtime_seconds
        self.mtime_nanoseconds = mtime_nanoseconds
        self.dev = dev
        self.ino = ino
        self.mode = mode
        self.uid = uid
        self.gid = gid
        self.size = size
        self.sha1 = sha1

        self.flags = flags
        self.assume_valid = bool(flags & (0b10000000 << 8))
        self.extended =     bool(flags & (0b01000000 << 8))
        self.stage_one =    bool(flags & (0b00100000 << 8))
        self.stage_two =    bool(flags & (0b00010000 << 8))

        self.extra_flags = extra_flags
        if self.extra_flags:
            self.reserved =         bool(extra_flags & (0b10000000 << 8))
            self.skip_worktree =     bool(extra_flags & (0b01000000 << 8))
            self.intent_to_add =     bool(extra_flags & (0b00100000 << 8))
        else:
            self.reserved = None
            self.skip_worktree = None
            self.intent_to_add = None