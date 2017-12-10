import os
import sys
import subprocess
import shutil

VALID_KEYWORDS = ("init", "add", "startdev", "enddev", "clean")

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
            sys.exit(1)

        # Read in everything in the file
        for line in file.read().split("\n"):

            def _add_file(self, path):
                """
                See if the file is an Arduino project file

                :param path: path to check
                :return:
                """
                # See if this is the arduino project file
                if len(path.strip()) > 4 and path.strip()[-4:] == ".ino":
                    # Make sure that an arduino project file hasn't been found already
                    if self.ardunio_file != None:
                        print("arudev: two .ino files tracked, exiting", file=sys.stderr)
                        sys.exit(1)
                    else:
                        self.ardunio_file = path.strip()
                else:
                    self.files.append(path.strip())
                pass
            # Empty line detection
            if len(line.strip()) == 0:
                continue

            # Comment detection
            if line.strip()[0] == '#':
                continue

            # Make sure the file (or directory) exists
            if not(os.path.exists(line.strip())):
                raise ParserFileNotFoundError("adudev: file `" + line.strip() + "` could not be found!")

            # Convert directories into files
            if os.path.isdir(line.strip()):
                def _find_file_r(self, path):
                    """
                    Recursive function to find all the files if a directory is given

                    :param path: the path to examine
                    """
                    # Base case
                    if os.path.isfile(path):
                        _add_file(self, path)
                    else:
                        # Recurse over every file in the directory
                        for npath in os.listdir(path):
                            _find_file_r(self, path + os.sep + npath)

                _find_file_r(self, line.strip())
            else:
                _add_file(self, line.strip())

        # Make sure the arduino project file was found
        if self.ardunio_file == None:
            print("arudev: no arduino project file (.ino) found, exiting", file=sys.stderr)
            sys.exit(1)

        # Make sure there are no files with the same name
        file_names = []
        for file in self.files:
            name = os.path.basename(file)
            if name in file_names:
                print("arudev: redundant file name: `" + name + "`", file=sys.stderr)
                sys.exit(1)
            else:
                file_names.append(name)
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

            # Copy all files to the dev directory
            for file in self.files:
                shutil.copy(file, dev_dir)

            # Copy the Arduino project file
            shutil.copy(self.ardunio_file, dev_dir)

            # Open the Arduino IDE
            subprocess.call("start " + self.ardunio_file, shell=True)
        elif slice[0] == "enddev":
            # Quick link to the development directory
            dev_dir = "dev" + os.sep + os.path.basename(self.ardunio_file)[:-4]

            # Make sure the dev directory exists
            if not(os.path.exists(dev_dir)):
                print("arudev: dev directory does not exist (have you run `startdev`?)", file=sys.stderr)
                sys.exit(1)

            # Copy files back to their home
            for file in self.files:
                shutil.copy(dev_dir + os.sep + os.path.basename(file), file)

            shutil.copy(dev_dir + os.sep + os.path.basename(self.ardunio_file), self.ardunio_file)
        elif slice[0] == "add":
            # Make sure we have enough arguments
            if len(slice) == 1:
                print("arudev: expected argument; exiting", file=sys.stderr)
                sys.exit(1)

            # Open the project file
            with open(".arudev", "a+") as f:
                for nfile in slice[1:]:
                    if os.path.exists(nfile):
                        f.write(nfile + "\n")
                    else:
                        print("arudev: file not found (`" + nfile + "`); continuing", file=sys.stderr)
        elif slice[0] == "clean":
            shutil.rmtree("dev" + os.sep)


class ParserFileNotFoundError(FileNotFoundError):
    """
    Exception raised when the Parser cannot find the specified file.
    """

    pass