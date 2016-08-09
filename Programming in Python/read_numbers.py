# Write program which reads the number of consoles (one per line)
# so long as the amount entered number not equal to 0,
# and then outputs the sum of squares of the read numbers
s = 0
d = 0
while True:
    a = int(input())
    s += a
    d += a*a
    if s == 0:
        break
print(d)