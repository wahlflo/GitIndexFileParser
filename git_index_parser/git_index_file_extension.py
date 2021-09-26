
class GitIndexFileExtension:
    def __init__(self, extension_number: int, signature: str, size: int, data: str):
        self.extension_number = extension_number
        self.signature = signature
        self.size = size
        self.data = data
