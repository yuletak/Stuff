listA = [0, 1, 2, 3, 4, 5, 6, 7]
listB = [0, 2, 4, 6, 8, 10]
listC = [1, 2, 3, 4, 10, 12, 13]
listD = []
count = {}

for a in listA:
    if a not in count.keys():
        count[a] = 0
    count[a] += 1

for b in listB:
    if b not in count.keys():
        count[b] = 0
    count[b] += 1

for c in listC:
    if c not in count.keys():
        count[c] = 0
    count[c] += 1

for k in count.keys():
    if count[k] == 2:
        listD.append(k)

print listD
