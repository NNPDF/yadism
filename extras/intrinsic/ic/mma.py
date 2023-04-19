import io
import subprocess
import threading


def writeall(p, res):
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
    """
    Calls Mathematica interactively from Python.
    """

    def __init__(self):
        self.p = subprocess.Popen(
            ["math", "-noprompt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )

    def send(self, code):
        """
        Sends some Mathematica code to the running terminal.

        An explicit `@` is added as the EOF signal to the thread worker.

        Parameters
        ----------
            code : str
                executed code
        """
        # reading needs to be on a seperate stream - idea from here:
        # https://stackoverflow.com/questions/19880190/interactive-input-output-using-python/53312631#53312631
        stream = io.StringIO()
        writer = threading.Thread(target=writeall, args=(self.p, stream))
        writer.start()

        self.p.stdin.write((code + 'Print["@"];\n').encode())
        self.p.stdin.flush()
        writer.join()
        stream.seek(0)
        s = stream.read()
        return s[1:-2].strip()

    def close(self):
        """Close the interactive terminal, by sending the `Exit[]` command."""
        self.send("Exit[];")
