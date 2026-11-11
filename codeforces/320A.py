c = input()
check_lis = ["1", "14", "144"]
for i in range(len(c)):
    if c[:i] in check_lis:
        continue
    if c[:i] not in check_lis:
        print("NO")