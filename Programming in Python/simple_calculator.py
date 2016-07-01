# Simple Calculator
# the user enters three lines:
# the first number, the second number, and the operation
# then applies to the operation of the entered numbers
a = float(input())
b = float(input())
o = input()
if (o == '+'):
  print(a+b)
elif (o == '-'):
  print(a-b)
elif (o == '/'):
  if (b == 0):
    print("Division by zero!")
  else:
    print(a/b)
elif (o == '*'):
  print(a*b)
elif (o == 'mod'):
  if (b == 0):
    print("Division by zero")
  else:
    print(a%b)
elif (o == 'pow'):
  print(a**b)
elif (o == 'div'):
  if (b == 0):
    print("Division by zero")
  else:
    print(a//b)