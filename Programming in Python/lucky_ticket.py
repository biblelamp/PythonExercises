# Lucky ticket
# The ticket is considered lucky if the sum of the first
# three digits equals the sum of the last three digits
# of the ticket number.
b = int(input())
s1 = b%10 + b%100//10 + b%1000//100
s2 = b%10000//1000 + b%100000//10000 + b//100000
if (s1 == s2):
  print("Lucky ticket")
else:
  print("Regular ticket")