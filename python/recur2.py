def fibonaci(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    return fibonaci(num-1) + fibonaci(num-2)

num = fibonaci(8)
print(num)