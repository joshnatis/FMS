import sys
fin = sys.argv[1]

ids=[]
with open(fin, "r") as f:
	strip=f.readline()
	for line in f:
		fields = line.split(",")
		ids.append(fields[0])
	print(ids)
