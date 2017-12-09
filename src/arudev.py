"""
Arduino Development Script

:author: Connor Henley, @thatging3rkid
"""
import os
import sys
import datetime
import traceback

from src.FileContents import FileContents, VALID_KEYWORDS, ParserFileNotFoundError


def main():
    """
    Main method; initialize objects and delegate work
    """

    ### Parse the arguments (who needs argparse?)
    # Start by making sure there are enough arguments
    if len(sys.argv) < 2:
        print("arudev: not enough arguments (use --help for help)", file=sys.stderr)
        exit(1)
    # See if the keyword is valid
    if not(sys.argv[1] in VALID_KEYWORDS):
        # Second keyword is asking for help
        if sys.argv[1] == "--help":
            print("arudev: an Arduino development script\n", file=sys.stderr)
            print("usage: arudev keyword [args]\n", file=sys.stderr)
            print("keyword: tells arudev what to do (ie `init` to initialize this directory)", file=sys.stderr)
            print("[args]: arguments processed with the keyword (if needed)", file=sys.stderr)
            exit(0)
        # Unknown keyword, so print an error
        else:
            print("arudev: unknown keyword `" + sys.argv[1] + "`", file=sys.stderr)
            exit(1)
    # Check to see if this is an init call
    if sys.argv[1] == "init":
        # Generate the file
        if not(os.path.exists(".arudev")):
            with open(".arudev", 'a') as f:
                f.write("# arudev project file\n")
                # See if the user put the program in quiet mode
                if not(len(sys.argv) >= 3 and sys.argv[2] == "-q"):
                    f.write("# Generated on: " + datetime.datetime.now().strftime("%x %X") + "\n")
            print("arudev: project initialized", file=sys.stderr)
            exit(0)
        else:
            print("arudev: project already initialized; doing nothing", file=sys.stderr)
            exit(1)



    # Try to open the arudev file
    fc = None
    try:
        with open(".arudev", mode="r") as f:
            fc = FileContents(f)
        fc.run(sys.argv[1:])
    except ParserFileNotFoundError as e:
        # File not found when parsing, so raise an error
        print(e, file=sys.stderr)
        exit(1)
    except FileNotFoundError as e:
        # .arudev file not found, so this is not an arudev directory
        print("arudev: invalid directory (no .arudev file)", file=sys.stderr)
        print(e)
        traceback.print_stack()
        exit(1)
    except Exception as e:
        # Some other exception happened, print it
        print(e, file=sys.stderr)
        traceback.print_exc(e)

main()