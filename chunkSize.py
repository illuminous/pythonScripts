def read_in_chunks(file_object, chunk_size=10024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


f = open('J:/event_prep/z16/cleanFiles/outfileclean.txt')
for piece in read_in_chunks(f):
    process_data(piece)
