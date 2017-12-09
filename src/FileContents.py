import os
import sys

import shutil

VALID_KEYWORDS = ("init", "add", "startdev", "enddev")

class FileContents():

    files = []
    ardunio_file = None

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

            # See if this is the arduino project file
            if len(line.strip()) > 4 and line.strip().replace("/","").replace("\\","")[-4:] == ".ino":
                # Make sure that an arduino project file hasn't been found already
                if self.ardunio_file != None:
                    print("arudev: two .ino files tracked, exiting", file=sys.stderr)
                    exit(1)
                else:
                    self.ardunio_file = line.strip()
            self.files.append(line.strip())

        # Make sure the arduino project file was found
        if self.ardunio_file == None:
            print("arudev: no arduino project file (.ino) found, exiting", file=sys.stderr)
            exit(1)
        pass


    def run(self, slice):
        # Check for an empty slice
        if len(slice) == 0:
            return

        ### Check to see what the user wants to do
        # startdev
        if slice[0] == "startdev":
            # Starting development is pretty easy, make a directory and copy everything in there
            dev_dir = "dev/" + os.path.basename(self.ardunio_file)[:-4]
            # Make sure the dev directory exists
            if not(os.path.exists(dev_dir)):
                os.makedirs(dev_dir)

            def _copyr(path):
                """
                Recursively copy everything to the dev directory
                :param path: directory to look in
                """
                # Base case
                if os.path.isfile(path):
                    shutil.copy(path, dev_dir)
                else:
                    # Call for all items in the dir
                    for npath in os.listdir(path):
                        _copyr(path + os.sep + npath)

            for file in self.files:
                _copyr(file)








class ParserFileNotFoundError(FileNotFoundError):
    """
    Exception raised when the Parser cannot find the specified file.
    """

    pass