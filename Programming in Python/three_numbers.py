# Three Numbers
# Write a program that takes as input three integer numbers, one number per line, and outputs to the console in the first three lines maximum, then the minimum, then the remaining number
a = int(input())
b = int(input())
c = int(input())
if (b>a):
  a,b = b,a
if (c>b):
  b,c = c,b
if (b>a):
  a,b = b,a
print(a)
print(c)
print(b)