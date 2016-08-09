# Print the matrix size n × n, filled with numbers from 1 to n*n
# spiral, leaving the top-left corner and twisted clockwise
# preparing
n = int(input())
a = [[0 for j in range(n+2)] for i in range(n+2)]
for i in range(n+2):
    a[i][0] = a[i][n+1] = a[0][i] = a[n+1][i]= 1
# filling
x = y = 1
count = 0
dx = 1
dy = 0
while (count < n**2):
    count += 1
    a[x][y] = count
    if (a[x+dx][y+dy] > 0):
        if (dx == 1):
            dx = 0
            dy = 1
        elif (dy == 1):
            dx = -1
            dy = 0
        elif (dx == -1):
            dx = 0
            dy = -1
        elif (dy == -1):
            dx = 1
            dy = 0
    x += dx
    y += dy
# output
for y in range(1,n+1):
    for x in range(1,n+1):
        print(a[x][y], end=' ') 
    print()