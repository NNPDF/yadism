import tinydb


db = tinydb.TinyDB("input.json")
theories_table = db.table("theories")

theories_table.insert({1: 2, 3: 4})
print(theories_table)
print(dir(theories_table), flush=True)

theories_table.purge()

theories_table.insert({1: 2, 3: 4})
