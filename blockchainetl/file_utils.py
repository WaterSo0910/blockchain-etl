# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import contextlib
import os
import pathlib
import sys
import shutil
import logging

import s3fs

s3 = s3fs.S3FileSystem()


def smart_copy_file(src, dst):
    assert os.path.isdir(dst)

    if src.startswith("s3://"):
        # FIXME: s3.get('aaa', '/tmp') returns None, but /tmp/aaa not exists
        s3.get(src, os.path.join(dst, os.path.basename(src)))
    else:
        # FIXME: in some cases, the source file is exists, but shutil.copy2 failed to copy:
        # stack: Traceback (most recent call last):
        #   File "blockchainetl/streaming/postgres_utils.py", line 166, in external_copy_file_into_redo # noqa
        #     smart_copy_file(file, redo_path)
        #   File "blockchainetl/file_utils.py", line 42, in smart_copy_file
        #     shutil.copy2(src, dst)
        #   File ".pyenv/versions/3.9.12/lib/python3.9/shutil.py", line 445, in copy2
        #     copystat(src, dst, follow_symlinks=follow_symlinks)
        #   File ".pyenv/versions/3.9.12/lib/python3.9/shutil.py", line 384, in copystat
        #     lookup("utime")(dst, ns=(st.st_atime_ns, st.st_mtime_ns),
        # FileNotFoundError: [Errno 2] No such file or directory
        try:
            shutil.copy2(src, dst)
        except FileNotFoundError as e:
            logging.error(f"failed to copy {src} into {dst} error: {e}")
            shutil.copy(src, dst)


# https://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely
@contextlib.contextmanager
def smart_open(filename=None, mode="w", binary=False, create_parent_dirs=True):
    fh = get_file_handle(filename, mode, binary, create_parent_dirs)

    try:
        yield fh
    finally:
        fh.close()


def get_file_handle(filename, mode="w", binary=False, create_parent_dirs=True):
    is_s3 = filename and filename.startswith("s3://")
    is_file = filename and not is_s3 and filename != "-"

    if create_parent_dirs and not is_s3 and filename is not None:
        dirname = os.path.dirname(filename)
        pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
    full_mode = mode + ("b" if binary else "")
    if is_s3:
        fh = s3.open(filename, full_mode)
    elif is_file:
        fh = open(filename, full_mode)
    elif filename == "-":
        fd = sys.stdout.fileno() if mode == "w" else sys.stdin.fileno()
        fh = os.fdopen(fd, full_mode)
    else:
        fh = NoopFile()
    return fh


def close_silently(file_handle):
    if file_handle is None:
        pass
    try:
        file_handle.close()
    except OSError:
        pass


class NoopFile:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        _exc_type, _exc_val, _exc_tb = _exc_type, _exc_val, _exc_tb
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def readable(self):
        pass

    def writable(self):
        pass

    def seekable(self):
        pass

    def read(self):
        pass

    def close(self):
        pass

    def write(self, _bytes):
        _bytes = _bytes
        pass
