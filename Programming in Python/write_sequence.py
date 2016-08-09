# Write a program that displays a portion of the sequence
# 1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 ...
# (the number is repeated many times, which is equal).
# The input program is passed a positive integer n -
# the many elements of the sequence must display program.
# The output is expected a sequence of numbers, separated by spaces.
n = int(input())
k = 0
c = 0
while True:
    k += 1
    for i in range(k):
        c += 1
        print(k, end=' ')
        if c == n:
            break
    if c == n:
        break