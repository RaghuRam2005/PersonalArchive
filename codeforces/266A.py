n = input()
check = ""
count = 0
x = input()
for s in x:
    if s is check:
        count += 1
    else:
        check = s
print(count)