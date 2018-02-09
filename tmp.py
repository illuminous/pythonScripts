import itertools

l = [[1,2,3],[4,5],[6,7,8,9],[0]]

for x in itertools.izip_longest(*l):
    print " ".join(str(i) for i in x)
