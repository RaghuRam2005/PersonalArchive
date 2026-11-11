inp_str = input()
if len(set(inp_str)) %2 == 0:
    print("CHAT WITH HER!")
elif len(set(inp_str)) %2 != 0:
    print("IGNORE HIM!")