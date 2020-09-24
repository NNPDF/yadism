class TableManager:
    """
    Wrapper to a single table

    Parameters
    ----------
        table : tinydb.Table
            table
    """
    def __init__(self, table):
        self.table = table

    def truncate(self):
        """Truncate all elements."""
        # deny rest
        if self.table.name != "logs":
            raise RuntimeError("only logs are allowed to be emptied by this interface!")
        # ask for confirmation
        if input("Purge all logs? [y/n]") != "y":
            print("Doing nothing.")
            return
        self.table.truncate()

    def all(self):
        """Retrieve all entries"""
        return self.table.all()

    def get(self, doc_id):
        """Retrieve an entry"""
        return self.table.get(doc_id=doc_id)
