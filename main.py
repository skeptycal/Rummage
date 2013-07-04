"""
Rummage (main)

Licensed under MIT
Copyright (c) 2011 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import wx
import sys
import argparse
import traceback
from os.path import abspath, exists, basename, dirname, join, normpath, isdir, isfile

from _lib.settings import Settings

from _gui.custom_app import CustomApp, set_debug_mode
from _gui.custom_app import debug, debug_struct, info, error
from _gui.rummage_dialog import RummageFrame
from _gui.regex_test_dialog import RegexTestDialog

__version__ = "1.0.0"


def parse_arguments():
    parser = argparse.ArgumentParser(prog='Rummage', description='A python grep like tool.')
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    parser.add_argument('--debug', '-d', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--searchpath', '-s', nargs=1, default=None, help="Path to search.")
    parser.add_argument('--regextool', '-r', action='store_true', default=False, help="Open just the regex tester.")
    return parser.parse_args()


def gui_main(script):
    Settings.load_settings()
    args = parse_arguments()
    if args.debug:
        set_debug_mode(True)
    app = CustomApp(redirect=True, single_instance_name="Rummage")
    if app.is_instance_okay() or not Settings.get_single_instance():
        if args.regextool:
            RegexTestDialog(None, False, False, stand_alone=True).Show()
        else:
            RummageFrame(None, script, args.searchpath[0] if args.searchpath is not None else None).Show()
    app.MainLoop()


if __name__ == "__main__":
    if sys.platform == "darwin" and len(sys.argv) > 1 and sys.argv[1].startswith("-psn"):
        script_path = join(dirname(abspath(sys.argv[0])), "..", "..", "..")
        del sys.argv[1]
    else:
        script_path = dirname(abspath(sys.argv[0]))

    sys.exit(gui_main(script_path))
