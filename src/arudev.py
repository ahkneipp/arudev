"""
Arduino Development Script (arudev)

:author: Connor Henley, @thatging3rkid
"""
import os
import sys
import shutil
import datetime
import traceback

try:
    from src.FileContents import FileContents, VALID_KEYWORDS, ParserFileNotFoundError
except ImportError as ie:
    from FileContents import FileContents, VALID_KEYWORDS, ParserFileNotFoundError


def main():
    """
	Main method; initialize objects and delegate work
    """


    ## Parse the arguments (who needs argparse?)
    # Start by making sure there are enough arguments
    if len(sys.argv) < 2:
		print("arudev: not enough arguments (use --help for help)", file=sys.stderr)
        sys.exit(1)

    # See if the keyword is valid
    if not (sys.argv[1] in VALID_KEYWORDS):
        # Second keyword is asking for help
        if sys.argv[1] == "--help":
	        print("arudev: an Arduino development script\n", file=sys.stderr)
            print("usage: arudev keyword [args]\n", file=sys.stderr)
            print("keyword: tells arudev what to do (ie `init` to initialize this directory)", file=sys.stderr)
            print("[args]: arguments processed with the keyword (if needed)\n", file=sys.stderr)
            print("list of keywords:", file=sys.stderr)
            print("    init: initializes a project for the first time, makes a .arudev file", file=sys.stderr)
            print("    start: makes the dev/ directory and tries to open Arduino IDE", file=sys.stderr)
            print("    end: moves files back to their original locations", file=sys.stderr)
            print("    add: adds files to be moved by arudev", file=sys.stderr)
            print("    clean: removes the temporary directory", file=sys.stderr)
            sys.exit(0)
	    # Unknown keyword, so print an error
        else:
            print("arudev: unknown keyword `" + sys.argv[1] + "`", file=sys.stderr)
	        sys.exit(1)
    ## Check to see if the first call is a file-call (operations that edit the file directly)
    # init
    if sys.argv[1] == "init":
        # Generate the file
        if not (os.path.exists(".arudev")):
            with open(".arudev", 'a') as f:
                f.write("# arudev project file\n")
	            f.write("# Generated on: " + datetime.datetime.now().strftime("%x %X") + "\n")
            print("arudev: project initialized", file=sys.stderr)
            sys.exit(0)
        else:
            print("arudev: project already initialized; doing nothing", file=sys.stderr)
            sys.exit(1)

    # add
    elif sys.argv[1] == "add":
        # Make sure we have enough arguments
        args = sys.argv[1:]
        if len(args) == 1:
            print("arudev: expected argument; exiting", file=sys.stderr)
            sys.exit(1)

        # Make sure .arudev exists
        if not os.path.exists(".arudev"):
            print("arudev: invalid directory (no .arudev file)", file=sys.stderr)
            sys.exit(1)

        # Open the project file
        with open(".arudev", "a+") as f:
            for newfile in args[1:]:
                if os.path.exists(newfile):
                    # Convert to Unix-esque paths
                    newfile = newfile.replace("\\", "/")
                    # Check for unnecessary file links
                    if newfile.startswith("./"):
                        newfile = newfile[2:]
                    f.write(newfile + os.linesep)
                else:
                    print("arudev: file not found (`" + newfile + "`); continuing", file=sys.stderr)
        sys.exit(0)

    # clean
    elif sys.argv[1] == "clean":
        shutil.rmtree("dev" + os.sep)
        sys.exit(0)

    # Try to open the arudev file
    try:
        with open(".arudev", "r") as f:
            fc = FileContents(f)
            fc.run(sys.argv[1:])
    except ParserFileNotFoundError as e:
        # File not found when parsing, so raise an error
        print(e, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        # .arudev file not found, so this is not an arudev directory
        print("arudev: invalid directory (no .arudev file)", file=sys.stderr)
        print(e)
        traceback.print_stack()
        sys.exit(1)
    except Exception as e:
        # Some other exception happened, print it
        print(e, file=sys.stderr)
        traceback.print_exc(e)


if __name__ == "__main__":
    main()
