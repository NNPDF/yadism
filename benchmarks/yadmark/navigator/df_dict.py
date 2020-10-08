class DFdict(dict):
    """
    TODO: translate in docs:
        output the table: since there are many table produced by this
        function output instead a suitable object
        the object should be iterable so you can explore all the values,
        but it has a __str__ (or __repr__?) method that will automatically
        loop and print if its dropped directly in the interpreter
    """

    def __init__(self, *args):
        super(DFdict, self).__init__(*args)
        self.msgs = []

    def print(self, *msgs, sep=" ", end="\n"):
        if len(msgs) > 0:
            self.msgs.append(msgs[0])

            for msg in msgs[1:]:
                self.msgs.append(sep)
                self.msgs.append(msg)
        self.msgs.append(end)

    def __setitem__(self, key, value):
        self.print(f"PID: {key}")
        self.print(value)
        self.print()
        super(DFdict, self).__setitem__(key, value)

    def __repr__(self):
        return "".join([str(x) for x in self.msgs])

    def to_document(self):
        """
        TinyDB compatibility layer
        """
        d = {}
        for k, v in self.items():
            d[k] = v.to_dict(orient="records")

        return d
