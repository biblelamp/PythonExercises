# Write a program, which is fed to the input of a rectangular matrix
# in the form of a sequence of rows, ending with a line containing
# only the string "end" (without quotes)
# The program must write a matrix of the same size, in which each
# element is in a position i, j is the sum of the elements of the
# first matrix in position (i-1, j), (i + 1, j), (i, j-1), (i , j + 1).
# In extreme element adjacent characters is on the opposite side of the matrix.
# In the case of a single row / column element is a neighbor to himself in the appropriate direction
# fill
m1 = []
m2 = []
while True:
    a = input().split()
    if a[0] == 'end':
        break
    else:
        m1 += [[int(i) for i in a]]
        m2 += [[int(i) for i in a]]
# are processing
for i in range(len(m1)):
    for j in range(len(m1[i])):
        i1 = i-1 if (i > 0) else len(m1)-1
        i2 = i+1 if (i < len(m1)-1) else 0
        j1 = j-1 if (j > 0) else len(m1[i])-1
        j2 = j+1 if (j < len(m1[i])-1) else 0
        m2[i][j] = m1[i1][j] + m1[i2][j] + m1[i][j1] + m1[i][j2]
        print(m2[i][j], end = ' ')
    print()