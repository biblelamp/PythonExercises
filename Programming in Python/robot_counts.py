# The robot which counts the number of programmers
# To it sounded right, for every n need to use the right end of the word.
n = int(input())
k = n % 10
m = n % 100
if ((10 < m < 15) or (k == 0) or (k > 4)):
  print(str(n)+" программистов")
elif ((k > 1) and (k < 5 )):
  print(str(n)+" программиста")
elif (k == 1):
  print(str(n)+" программист")