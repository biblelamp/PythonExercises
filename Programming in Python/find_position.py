# Write a program that reads a list lst numbers from the first row
# and the number x of the second line, which displays all items in
# which is found the number x in the transmitted list lst
# Positions are numbered from zero, if the number x
# does not appear in the list, display the string "Отсутствует"
# (without the quotation marks, with a capital letter).
lst = [int(i) for i in input().split()]
x = int(input())
f = True
for i in range(len(lst)):
    if lst[i] == x:
        print(i, end= ' ')
        f = False
if f:
    print('Отсутствует')