'''
factorial of the number
'''
def fact(n):
    if n==1:
        return 1
    return n * fact(n-1)

factorial = fact(5)
print(factorial)