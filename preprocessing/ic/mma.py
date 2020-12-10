# -*- coding: utf-8 -*-
import re
import subprocess
import threading
import io


def writeall(p, res):
    while True:
        # print("read data: ")
        data = p.stdout.read(1).decode("utf-8")
        if not data or data == "@":
            break
        res.write(data)
        res.flush()


class MmaRunner:
    def __init__(self):
        self.p = subprocess.Popen(
            ["math", "-noprompt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )

    def send(self, code):
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
        self.send("Exit[];")


def prepare(fform):
    fform = re.sub("\n *\\d", "", fform)
    fform = fform.replace("d0", "")
    fform = fform.replace("s1h2", "s1h**2")
    fform = fform.replace("Del2", "Del**2")
    fform = fform.replace("Delp2", "Delp**2")
    fform = fform.replace("**", "^")
    return fform
