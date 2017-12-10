# arudev

Development scripts for use with Arduino IDE (aka **Ar**d**u**ino **Dev**eloplopment scripts).

## Installation

To install globally (on Windows), it's easiest to compile arudev to an executable (not python script). Luckily, a precompiled binary can be found under the releases tab.

#### Manual compilation

First, PyWin32 needs to be installed (making sure your default python version and bit-width (32 vs 64 bit) (run `py` in console to see it) matches the version of python you have installed), then using `pip` to install `pyinstaller`. Then, running `pyinstaller src/arudev.py` at the top level directory makes a /build (for development) and /dist (what is used and distributed).

#### Installing globally

With a self-compiled /dist or a precompiled zip file, extract (or copy) the code to a local directory (ie C:\Users\<username>\bin\arudev-win-amd64-v0.1c), then add that path to the PATH environment variable (start>explorer (right click)>more>properties>advanced system settings>environment variables; on newer Windows versions, you can go under User Variables and add a new entry).
