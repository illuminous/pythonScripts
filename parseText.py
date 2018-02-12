import string
pattern = "A.S.I."
for line in open("c:/WorkSpace/shaleExperts/automation/drillPermits.txt","r"):
    columns = line.split(",")

    new = columns[9].translate(None, '.,*')
    print columns[9], '-',new.upper()


