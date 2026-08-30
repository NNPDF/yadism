"""Python interface to Mathematica via the CLI."""

import io
import shutil
import subprocess
import threading
from typing import Self


def _thread_writer(p: subprocess.Popen, res: io.StringIO) -> None:
    """
    Thread worker.

    Reads from the stdout of the subprocess until it is closed or an `@` is
    encountered.

    Parameters
    ----------
        p : subprocess.Popen
            subprocess
        res : stream
            stream to which the output is copied
    """
    while True:
        # print("read data: ")
        data = p.stdout.read(1).decode("utf-8")
        if not data or data == "@":
            break
        res.write(data)
        res.flush()


class MmaRunner:
    """Call Mathematica interactively from Python via the CLI."""

    p: subprocess.Popen
    """CLI thread"""

    def __enter__(self: Self) -> Self:
        path = shutil.which("math")
        assert path is not None
        self.p = subprocess.Popen(
            [path, "-noprompt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        return self

    def send(self: Self, code: str) -> str:
        """Send Mathematica code to the running CLI.

        An explicit `@` is added as the EOF signal to the thread worker.
        """
        # reading needs to be on a seperate stream - idea from here:
        # https://stackoverflow.com/questions/19880190/interactive-input-output-using-python/53312631#53312631
        stream = io.StringIO()
        writer = threading.Thread(target=_thread_writer, args=(self.p, stream))
        writer.start()

        self.p.stdin.write((code + 'Print["@"];\n').encode())
        self.p.stdin.flush()
        writer.join()
        stream.seek(0)
        s = stream.read()
        return s[1:-2].strip()

    def __exit__(self: Self, exc_type: type, _exc_value, _traceback):
        """Close the interactive CLI, by sending the `Exit[]` command."""
        if exc_type is not None:
            return
        if self.p is not None:
            self.send("Exit[];")
            self.p.terminate()
