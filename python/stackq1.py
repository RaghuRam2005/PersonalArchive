def asteroid_collison(asteroids):
    stack = []
    for x in asteroids:
        if (x < 0 and not stack) or (x < 0 and stack[-1] < 0) or (x > 0) or (not stack):
            stack.append(x)
        elif (x < 0 and stack[-1] < abs(x)):
            while stack and stack[-1] > 0 and stack[-1] < abs(x):
                stack.pop()
            if not stack or stack[-1] < 0:
                stack.append(x)
        elif (x < 0 and stack[-1] == abs(x)):
            stack.pop()
            if not stack or stack[-1] < 0:
                stack.append(x)
    return stack

asteroids = [-1,-1,1,-1,5]
print(asteroid_collison(asteroids))
