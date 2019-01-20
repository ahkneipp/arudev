import os
import sys
import shutil
import subprocess

VALID_KEYWORDS = ("init", "add", "start", "startdev", "end", "enddev", "clean")


class FileContents:

    files = []
    ardunio_file = None

    def __init__(self, file):
        """
        Initialize a FileContents object
        :param file: a file to read data from
        """

        # None check
        if file is None:
            print("file is None!", file=sys.stderr)
            sys.exit(1)

        # Read in everything in the file
        for line in file.read().split("\n"):

            def _add_file(s_self, path):
                """
                See if the file is an Arduino project file

                :param path: path to check
                :return:
                """
                # See if this is the arduino project file
                if len(path.strip()) > 4 and path.strip()[-4:] == ".ino":
                    # Make sure that an arduino project file hasn't been found already
                    if s_self.ardunio_file is not None:
                        print("arudev: two .ino files tracked, exiting", file=sys.stderr)
                        sys.exit(1)
                    else:
                        s_self.ardunio_file = path.strip()
                else:
                    s_self.files.append(path.strip())
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
                def _find_file_r(s_self, path):
                    """
                    Recursive function to find all the files if a directory is given

                    :param path: the path to examine
                    """
                    # Base case
                    if os.path.isfile(path):
                        _add_file(s_self, path)
                    else:
                        # Recurse over every file in the directory
                        for npath in os.listdir(path):
                            _find_file_r(s_self, path + os.sep + npath)

                _find_file_r(self, line.strip())
            else:
                _add_file(self, line.strip())

        # Make sure the arduino project file was found
        if self.ardunio_file is None:
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

    def run(self, args):
        # Check for an empty slice
        if len(args) == 0:
            return

        ## Check to see what the user wants to do
        # startdev
        if args[0] == "startdev" or args[0] == "start":
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
            if sys.platform == "linux" or sys.platform == "linux2":
                ret = subprocess.call("arduino " + dev_dir + os.sep + os.path.basename(self.ardunio_file) + " &", shell=True,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # Check to see if Arduino IDE could be found
                if ret != 0:
                    print("arudev: Arduino IDE cannot be opened, continuing", file=sys.stderr)
            elif sys.platform == "darwin":
                subprocess.call("open -n " + dev_dir + os.sep + os.path.basename(self.ardunio_file), shell=True)
            elif sys.platform == "win32" or sys.platform == "win64":
                subprocess.call("start " + dev_dir + os.sep + os.path.basename(self.ardunio_file), shell=True)
            else:
                print("arudev: unknown OS, not trying to open file", sys.stderr)

        # enddev
        elif args[0] == "enddev" or args[0] == "end":
            # Quick link to the development directory
            dev_dir = "dev" + os.sep + os.path.basename(self.ardunio_file)[:-4]

            # Make sure the dev directory exists
            if not(os.path.exists(dev_dir)):
                print("arudev: dev directory does not exist (have you run `start`?)", file=sys.stderr)
                sys.exit(1)

            # Copy files back to their home
            for file in self.files:
                shutil.copy(dev_dir + os.sep + os.path.basename(file), file)

            shutil.copy(dev_dir + os.sep + os.path.basename(self.ardunio_file), self.ardunio_file)


class ParserFileNotFoundError(FileNotFoundError):
    """
    Exception raised when the Parser cannot find the specified file.
    """

    pass
