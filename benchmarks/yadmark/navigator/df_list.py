class DFlist(list):
    """
    TODO: translate in docs:
        output the table: since there are many table produced by this
        function output instead a suitable object
        the object should be iterable so you can explore all the values,
        but it has a __str__ (or __repr__?) method that will automatically
        loop and print if its dropped directly in the interpreter
    """

    def __init__(self, *args):
        super(DFlist, self).__init__(*args)
        self.msgs = []

    def print(self, *msgs, sep=" ", end="\n"):
        if len(msgs) > 0:
            self.msgs.append(msgs[0])

            for msg in msgs[1:]:
                self.msgs.append(sep)
                self.msgs.append(msg)
        self.msgs.append(end)

    def register(self, table):
        self.print(table)
        self.append(table)

    def __repr__(self):
        return "".join([str(x) for x in self.msgs])
