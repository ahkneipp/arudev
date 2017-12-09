import os
import sys

VALID_KEYWORDS = ("init", "add", "commit", "startdev", "enddev")

class FileContents():

    files = []

    def __init__(self, file):
        """
        Initialize a FileContents object
        :param file: a file to read data from
        """

        # None check
        if (file == None):
            print("file is None!", file=sys.stderr)
            exit(1)

        # Read in everything in the file
        for line in file.read().split("\n"):
            # Empty line detection
            if len(line.strip()) == 0:
                continue

            # Comment detection
            if line.strip()[0] == '#':
                continue

            # Make sure the file (or directory) exists
            if not(os.path.exists(line.strip())):
                raise ParserFileNotFoundError("adudev: file `" + line.strip() + "` could not be found!")

            self.files.append(line.strip())
        pass


    def run(self, slice):
        pass



class ParserFileNotFoundError(FileNotFoundError):
    pass