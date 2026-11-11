s = input()
c = s[:1]
s = s[1:]
if c.islower():
    c = c.upper()
s = c + s
print(s)