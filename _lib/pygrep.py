"""
pygrep

Licensed under MIT
Copyright (c) 2011 Isaac Muse <isaacmuse@gmail.com>
https://gist.github.com/facelessuser/5757669

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import threading
import sys
import re
from os import walk
from fnmatch import fnmatch
from os.path import isdir, join, abspath, basename, getsize, getmtime
from os.path import getctime as get_creation_time
from time import sleep
import struct
import traceback
import codecs
from file_hidden import is_hidden
from ctypes import *
import struct

import _lib.ure as ure
import _lib.text_decode as text_decode

LITERAL = 1
IGNORECASE = 2
DOTALL = 4
RECURSIVE = 8
FILE_REGEX_MATCH = 16
DIR_REGEX_MATCH = 32
BUFFER_INPUT = 64

_LOCK = threading.Lock()
_FILES = []
_RUNNING = False
_STARTED = False
_ABORT = False

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"

LINE_ENDINGS = ure.compile(r"(?:(\r\n)|(\r)|(\n))")
HEX_TX_TABLE = ("." * 32) + "".join(chr(c) for c in xrange(32, 127)) + ("." * 129)


# http://stackoverflow.com/questions/946967/get-file-creation-time-with-python-on-mac
class struct_timespec(Structure):
    _fields_ = [('tv_sec', c_long), ('tv_nsec', c_long)]


if _PLATFORM == "osx":
    class struct_stat64(Structure):
        _fields_ = [
            ('st_dev', c_int32),
            ('st_mode', c_uint16),
            ('st_nlink', c_uint16),
            ('st_ino', c_uint64),
            ('st_uid', c_uint32),
            ('st_gid', c_uint32),
            ('st_rdev', c_int32),
            ('st_atimespec', struct_timespec),
            ('st_mtimespec', struct_timespec),
            ('st_ctimespec', struct_timespec),
            ('st_birthtimespec', struct_timespec),
            ('dont_care', c_uint64 * 8)
        ]


    libc = CDLL('libc.dylib')
    stat64 = libc.stat64
    stat64.argtypes = [c_char_p, POINTER(struct_stat64)]


def getctime(pth):
    if _PLATFORM == "osx":
        # Get the appropriate creation time on OSX
        buf = struct_stat64()
        rv = stat64(pth.encode("utf-8"), pointer(buf))
        if rv != 0:
            raise OSError("Couldn't stat file %r" % pth)
        return buf.st_birthtimespec.tv_sec
    else:
        # Get the creation time for everyone else
        return get_creation_time(pth)


def threaded_walker(
    directory, file_pattern, file_regex_match,
    folder_exclude, dir_regex_match, recursive,
    show_hidden, size, modified, created
):
    global _RUNNING
    global _STARTED
    with _LOCK:
        _RUNNING = True
        _STARTED = True
    try:
        walker = _DirWalker(
            directory, file_pattern, file_regex_match,
            folder_exclude, dir_regex_match, recursive,
            show_hidden, size, modified, created
        )
        walker.run()
    except:
        print(str(traceback.format_exc()))
        pass
    with _LOCK:
        _RUNNING = False


def _re_pattern(pattern, ignorecase=False, dotall=False, multiline=True):
    flags = ure.UNICODE
    if multiline:
        flags |= ure.MULTILINE
    if ignorecase:
        flags |= ure.IGNORECASE
    if dotall:
        flags |= ure.DOTALL
    return ure.compile(pattern, flags)


def _literal_pattern(pattern, ignorecase=False, dotall=False, multiline=True):
    flags = ure.UNICODE
    if multiline:
        flags |= ure.MULTILINE
    if ignorecase:
        flags |= ure.IGNORECASE
    if dotall:
        flags |= ure.DOTALL
    return ure.compile(ure.escape(pattern), flags)


class GrepException(Exception):
    pass


class _FindRegion(object):
    def __init__(self, start, end):
        """
        Initialize find region result object.
        """

        self.__find_range = [start, end]

    def start(self):
        """
        Return start of find region result.
        """

        return self.__find_range[0]

    def end(self):
        """
        Return end of find region result.
        """

        return self.__find_range[1]


class _FileSearch(object):
    def __init__(self, pattern, flags, context, truncate_lines):
        self.literal = bool(flags & LITERAL)
        self.ignorecase = bool(flags & IGNORECASE)
        self.dotall = bool(flags & DOTALL)
        self.truncate_lines = truncate_lines
        if self.truncate_lines:
            self.context = (0, 0)
        else:
            self.context = context

        # Prepare search
        self.pattern = _literal_pattern(pattern, self.ignorecase) if self.literal else _re_pattern(pattern, self.ignorecase, self.dotall)
        self.find_method = self.pattern.finditer

    def __tx_bin(self, content):
        def_struct = lambda content: struct.Struct("=" + ("B" * len(content))).unpack(content)
        return content.translate(HEX_TX_TABLE)

    def __get_lines(self, content, m, binary=False):
        """
        Return the full line(s) of code of the found region.
        """

        start = m.start()
        end = m.end()
        bfr_end = len(content) - 1
        before = 0
        after = 0

        while start > 0:
            if content[start - 1] != "\n":
                start -= 1
            elif before >= self.context[0]:
                break
            else:
                before += 1
                start -= 1

        while end < bfr_end:
            if content[end] != "\n":
                end += 1
            elif after >= self.context[1]:
                break
            else:
                after += 1
                end += 1

        match_start = m.start() - start
        match_end = match_start + m.end() - m.start()
        if self.truncate_lines:
            length = end - start
            if length > 256:
                end = start + 256
                length = 256

            if match_start > length:
                match_start = length
            if match_end > length:
                match_end = 256
        return content[start:end] if not binary else self.__tx_bin(content[start:end]), (match_start, match_end), (before, after)

    def __findall(self, file_content):
        for m in self.find_method(file_content):
            yield m

    def __get_col(self, content, absolute_col, line_ending):
        col = 1
        for x in reversed(range(0, absolute_col)):
            if content[x] == line_ending:
                break
            col += 1
        return col

    def search(self, target, file_content, max_count=None, binary=False):
        """
        Search target file or buffer returning a generator of results.
        """

        ending = LINE_ENDINGS.search(file_content)
        line_ending = "\n"
        if ending is not None:
            if ending.group(2):
                line_ending = "\r"

        results = {"name": target, "count": 0, "line_ending": line_ending, "error": None, "results": []}

        for m in self.__findall(file_content):
            if max_count != None:
                if max_count == 0:
                    break
                else:
                    max_count -= 1

            result = {
                "lineno": file_content.count(line_ending, 0, m.start()) + 1,
                "colno": self.__get_col(file_content, m.start(), line_ending)
            }
            result["lines"], result["match"], result["context_count"] = self.__get_lines(file_content, m, binary)
            results["results"].append(result)
            results["count"] += 1

        return results


class _DirWalker(object):
    def __init__(
            self, directory, file_pattern, file_regex_match,
            folder_exclude, dir_regex_match, recursive,
            show_hidden, size, modified, created
        ):
        self.dir = directory
        self.size = (size[0], size[1] * 1024) if size is not None else size
        self.modified = modified
        self.created = created
        self.file_pattern = file_pattern
        self.file_regex_match = file_regex_match
        self.dir_regex_match = dir_regex_match
        self.folder_exclude = folder_exclude
        self.recursive = recursive
        self.show_hidden = show_hidden
        self.files = []

    def __is_hidden(self, path):
        if not self.show_hidden:
            return is_hidden(path)
        return False

    def __compare_value(self, limit_check, current):
        value_okay = False
        qualifier = limit_check[0]
        limit = limit_check[1]
        if qualifier == "eq":
            if current == limit:
                value_okay = True
        elif qualifier == "lt":
            if current < limit:
                value_okay = True
        elif qualifier == "gt":
            if current > limit:
                value_okay = True
        return value_okay

    def __is_times_okay(self, pth):
        times_okay = False
        mod_okay = False
        cre_okay = False
        self.modified_time = getmtime(pth)
        self.created_time = getctime(pth)
        if self.modified is None:
            mod_okay = True
        else:
            mod_okay = self.__compare_value(self.modified, self.modified_time)
        if self.created is None:
            cre_okay = True
        else:
            cre_okay = self.__compare_value(self.created, self.created_time)
        if mod_okay and cre_okay:
            times_okay = True
        return times_okay

    def __is_size_okay(self, pth):
        size_okay = False
        self.current_size = getsize(pth)
        if self.size is None:
            size_okay = True
        else:
            size_okay = self.__compare_value(self.size, self.current_size)
        return size_okay

    def __valid_file(self, base, name):
        """
        Returns whether a file can be searched.
        """

        try:
            valid = False
            if self.file_pattern != None and not self.__is_hidden(join(base, name)):
                if self.file_regex_match:
                    valid = True if self.file_pattern.match(name) != None else False
                else:
                    matched = False
                    exclude = False
                    for p in self.file_pattern:
                        if len(p) > 1 and p[0] == "-":
                            if fnmatch(name.lower(), p[1:]):
                                exclude = True
                                break
                        elif fnmatch(name.lower(), p):
                            matched = True
                    if exclude:
                        valid = False
                    elif matched:
                        valid = True
                if valid:
                    valid = self.__is_size_okay(join(base, name))
                if valid:
                    valid = self.__is_times_okay(join(base, name))
        except:
            valid = False
        return valid

    def __valid_folder(self, base, name):
        """
        Returns whether a folder can be searched.
        """

        valid = True
        try:
            if not self.recursive:
                valid = False
            elif self.__is_hidden(join(base, name)):
                valid = False
            elif self.folder_exclude != None:
                if self.dir_regex_match:
                    valid = False if self.folder_exclude.match(name) != None else True
                else:
                    matched = False
                    exclude = False
                    for p in self.folder_exclude:
                        if len(p) > 1 and p[0] == "-":
                            if fnmatch(name.lower(), p[1:]):
                                matched = True
                                break
                        elif fnmatch(name.lower(), p):
                            exclude = True
                    if matched:
                        valid = True
                    elif exclude:
                        valid = False
        except:
            valid = False
        return valid

    def run(self):
        global _FILES
        global _ABORT
        with _LOCK:
            _FILES = []
        for base, dirs, files in walk(self.dir):
            # Remove child folders based on exclude rules
            [dirs.remove(name) for name in dirs[:] if not self.__valid_folder(base, name)]

            # Seach files if they were found
            if len(files):
                # Only search files in that are in the inlcude rules
                for f in [(name, self.current_size, self.modified_time, self.created_time) for name in files[:] if self.__valid_file(base, name)]:
                    with _LOCK:
                        _FILES.append((join(base, f[0]), f[1], f[2], f[3]))
                    if _ABORT:
                        break
            if _ABORT:
                with _LOCK:
                    _ABORT = False
                break


class Grep(object):
    def __init__(
        self, target, pattern, file_pattern=None, folder_exclude=None,
        flags=0, context=(0, 0), max_count=None,
        show_hidden=False, all_utf8=False, size=None,
        modified=None, created=None, text=False, truncate_lines=False
    ):
        """
        Initialize Grep object.
        """

        global _RUNNING
        global _ABORT
        with _LOCK:
            if not _RUNNING and _ABORT:
                _ABORT = False
            if _RUNNING:
                raise GrepException("Grep process already running!")

        self.search = _FileSearch(pattern, flags, context, truncate_lines)
        self.buffer_input = bool(flags & BUFFER_INPUT)
        self.all_utf8 = all_utf8
        self.current_encoding = None
        self.idx = -1
        self.target = abspath(target) if not self.buffer_input else target
        self.max = max_count
        self.process_binary = text
        file_regex_match = bool(flags & FILE_REGEX_MATCH)
        dir_regex_match = bool(flags & DIR_REGEX_MATCH)
        self.kill = False
        self.thread = None
        self.is_binary = False
        if not self.buffer_input and isdir(self.target):
            self.thread = threading.Thread(
                target=threaded_walker,
                args=(
                    self.target,
                    self.__get_file_pattern(file_pattern, file_regex_match),
                    file_regex_match,
                    self.__get_dir_pattern(folder_exclude, dir_regex_match),
                    dir_regex_match,
                    bool(flags & RECURSIVE),
                    show_hidden,
                    size,
                    modified,
                    created
                )
            )
            self.thread.setDaemon(True)

    def __get_dir_pattern(self, folder_exclude, dir_regex_match):
        pattern = None
        if folder_exclude != None:
            pattern = ure.compile(folder_exclude, ure.IGNORECASE) if dir_regex_match else [f.lower() for f in folder_exclude.split("|")]
        return pattern

    def __get_file_pattern(self, file_pattern, file_regex_match):
        pattern = None
        if file_pattern != None:
            pattern = ure.compile(file_pattern, ure.IGNORECASE) if file_regex_match else [f.lower() for f in file_pattern.split("|")]
        return pattern

    def __decode_file(self, filename):
        bfr, self.current_encoding = text_decode.guess(filename)
        if self.current_encoding == "BIN":
            self.is_binary = True
        return bfr

    def __is_binary(self, content):
        length = 512 if len(content) > 512 else len(content)
        self.is_binary = re.search(b"[\x00]{2}", content[0:length]) is not None
        return self.is_binary

    def __has_bom(self, content):
        bom = None
        if content[:3] == codecs.BOM_UTF8:
            bom = "utf-8-sig"
        if content[:2] in [codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE]:
            bom = "utf-16"
        return bom

    def __read_file(self, file_name):
        content = None
        self.current_encoding = "BIN"
        self.is_binary = False
        # Force UTF for all
        if self.all_utf8:
            try:
                self.current_encoding = "UTF8"
                with codecs.open(file_name, encoding="utf-8-sig", errors="replace") as f:
                    content = f.read()
                    return content
            except:
                # print(str(traceback.format_exc()))
                pass
            return None

        # Non-Lazy decoding
        try:
            return self.__decode_file(file_name)
        except Exception:
            print(str(traceback.format_exc()))
            return None
        # Lazy decoding
        # encodings = [
        #     "ascii",
        #     "utf-8-sig",
        #     "utf-16",
        #     "latin-1"
        # ]
        # encodings_map = {
        #     0: "ASCII",
        #     1: "UTF8",
        #     2: "UTF16",
        #     3: "LATIN-1"
        # }
        # content = None
        # try:
        #     with open(file_name, "rb") as f:
        #         content = f.read()
        #         count = 0
        #         encode = self.__has_bom(content)
        #         if encode is not None:
        #             self.current_encoding = encodings_map[encodings.index(encode)]
        #             try:
        #                 return unicode(content, encode)
        #             except:
        #                 # print(str(traceback.format_exc()))
        #                 self.is_binary = True
        #                 self.current_encoding = "BIN"
        #         elif self.__is_binary(content):
        #             self.current_encoding = "BIN"
        #         else:
        #             for encode in encodings:
        #                 self.current_encoding = encodings_map[count]
        #                 self.is_binary = False
        #                 try:
        #                     return unicode(content, encode)
        #                 except:
        #                     # print(str(traceback.format_exc()))
        #                     self.is_binary = True
        #                     self.current_encoding = "BIN"
        #                     pass
        #                 count += 1

        # except Exception:
        #     # print(str(traceback.format_exc()))
        #     pass
        # if not self.process_binary:
        #     content = None
        # Unknown encoding, maybe binary, something else?
        return content

    def get_status(self):
        if self.thread is not None:
            return self.idx + 1 if self.idx != -1 else 0, len(_FILES)
        else:
            return 1, 1

    def abort(self):
        global _ABORT
        with _LOCK:
            _ABORT = True
        self.kill = True

    def find(self):
        """
        Walks through a given directory searching files via the provided pattern.
        If given a file directly, it will search the file only.
        Return the results of each file via a generator.
        """
        global _STARTED
        max_count = int(self.max) if self.max != None else None

        if self.thread is not None:
            self.idx = -1
            self.thread.start()
            done = False
            # Try to wait in case the
            # "is running" check happens too quick
            while not _STARTED:
                sleep(0.3)
            with _LOCK:
                _STARTED = False

            while not done:
                file_info = None
                while file_info is None:
                    if _RUNNING:
                        if len(_FILES) - 1 > self.idx:
                            self.idx += 1
                            file_info = _FILES[self.idx]
                        else:
                            sleep(0.3)
                    else:
                        if len(_FILES) - 1 > self.idx and not self.kill:
                            self.idx += 1
                            file_info = _FILES[self.idx]
                        elif self.kill:
                            break
                        else:
                            done = True
                            break

                if file_info is None:
                    done = True
                else:
                    file_name = file_info[0]
                    sz = file_info[1]
                    try:
                        content = self.__read_file(file_name)
                        if content == None:
                            continue
                        result = self.search.search(file_name, content, max_count, self.is_binary)
                        result["size"] = '%.2fKB' % (float(sz) / 1024.0)
                        result["encode"] = self.current_encoding
                        result["m_time"] = file_info[2]
                        result["c_time"] = file_info[3]
                    except:
                        results = {"name": file_name, "count": 0, "line_ending": None, "error": str(traceback.format_exc()), "results": []}
                        yield results
                    yield result
                    if max_count != None:
                        max_count -= result["count"]
                        if max_count == 0:
                            done = True
        elif self.buffer_input:
            # Perform search
            try:
                result = self.search.search("buffer input", self.target, max_count, False)
                result["size"] = "--"
                result["encode"] = "--"
                result["m_time"] = "--"
                result["c_time"] = "--"
                yield result
            except:
                results = {"name": "buffer input", "count": 0, "line_ending": None, "error": str(traceback.format_exc()), "results": []}
                yield results
        else:
            # Perform search
            file_name = self.target
            try:
                content = self.__read_file(file_name)
                if content != None:
                    result = self.search.search(file_name, content, max_count, self.is_binary)
                    result["size"] = "%.2fKB" % (float(getsize(file_name)) / 1024.0)
                    result["encode"] = self.current_encoding
                    result["m_time"] = getmtime(file_name)
                    result["c_time"] = getctime(file_name)
                    yield result
            except:
                results = {"name": file_name, "count": 0, "line_ending": None, "error": str(traceback.format_exc()), "results": []}
                yield results
