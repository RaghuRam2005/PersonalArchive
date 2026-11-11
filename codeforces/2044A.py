i = int(input())
res = [0]*i
for j in range(i):
    n = int(input())
    for a in range(1, n):
        for b in range(n):
            if a == n - b:
                res[j] += 1
for x in res:
    print(x)
