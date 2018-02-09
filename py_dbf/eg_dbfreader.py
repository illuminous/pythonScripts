from _DBF_Reader import dbfreader


filename="test.dbf"
f = open(filename, 'rb')
db = list(dbfreader(f))
f.close()
for record in db:
    print record
#fieldnames, fieldspecs, records = db[0], db[1], db[2:]

