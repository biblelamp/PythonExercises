class table_obj:
    ''' Таблица для крестиков-ноликов '''
    table = []

    def __init__(self):
        self.table = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

    ''' Очистка таблицы '''
    def clear(self):
        for y in [0, 1, 2]:
            for x in [0, 1, 2]:
                self.table[y][x] = "."

    def save(self, ini_file):
        str = ""
        for y in [0, 1, 2]:
            for x in [0, 1, 2]:
                str += self.table[x][y] + ","
        file = open(ini_file,'w')
        file.write(str)
        file.close()

    def read_file(self, ini_file):
        i = 0
        file = open(ini_file, 'r')
        str = file.read()
        strr = str.split(',')
        for y in [0, 1, 2]:
            for x in [0, 1, 2]:
                self.table[x][y] = strr[i]
                i += 1
        file.close()

    def get(self, y ,x):
        return self.table[y][x]

    def set(self, y, x, char):
        self.table[y][x] = char

    def is_full(self):
        for row in self.table:
            for cell in row:
                if cell == '.':
                    return False
        return True

    def is_win(self, ch):
        for i in [0, 1, 2]:
            if self.table[i][0] == ch and self.table[i][1] == ch and self.table[i][2] == ch:
                return True
            if self.table[0][i] == ch and self.table[1][i] == ch and self.table[2][i] == ch:
                return True
        if (self.table[0][0] == ch and self.table[1][1] == ch and self.table[2][2] == ch) or (self.table[2][0] == ch and self.table[1][1] == ch and self.table[0][2] == ch):
            return True
        return False;

    def __draw_o(self, canvas, x, y):
        canvas.create_oval(x * 200 + 50, y * 200 + 50, x * 200 + 150, y * 200 + 150, width = 5, outline = 'blue')

    def __draw_x(self, canvas, x, y):
        canvas.create_line(x * 200, y * 200, x * 200 + 200, y * 200 + 200, width = 5, fill = 'red')
        canvas.create_line(x * 200 + 200, y * 200, x * 200 , y * 200 + 200, width = 5, fill = 'red')

    def draw(self, canvas):
        for y in [0, 1, 2]:
            for x in [0, 1, 2]:
                if self.table[y][x] == 'X':
                    self.__draw_x(canvas, x, y)
                if self.table[y][x] == 'O':
                    self.__draw_o(canvas, x, y)