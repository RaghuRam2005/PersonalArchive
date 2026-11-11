i = int(input())
res = []
for _ in range(i):
    s = str(input())
    b = ""
    for x in s:
        if x == 'q':
            b += "p"
        elif x == 'p':
            b += 'q'
        else:
            b += x
    res.append(b)
for x in res:
    print(x)