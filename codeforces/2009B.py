n = int(input())
result = []
for x in range(n):
    a = int(input("a"))
    c = None
    res = []
    for i in range(a):
        c[i] = input()
    for i in range(a, 0, -1):
        for j in range(a):
            if c[i][j] == "#":
                res.append(j+1)
    result.append(res)

for i in result:
    for x in i:
        print(x, end=" ")
    print()