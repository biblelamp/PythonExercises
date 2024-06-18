from tkinter import *
from tkinter import messagebox
import random
import sys

table = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

def click_b1(event):
    x = event.x
    y = event.y
    int_x = int(x / 200)
    int_y = int(y / 200)
    s = "Mouse click x={} y={}".format(int_x, int_y)
    gui.title(s)
    if table[int_y][int_x] == ".":
        table[int_y][int_x] = "X"
        draw_table()
        if not x_win("X") :
            if not is_table_full():
                turn_AI()
                draw_table()
                if x_win("O") :
                    messagebox.showinfo("Information", "You lose")
                    retry()

            else:
                messagebox.showinfo("Information", "Draw")
                retry()

        else:
            messagebox.showinfo("Information", "You win")
            retry()

def is_table_full():
    for row in table:
        for cell in row:
            if cell == '.':
                return False
    return True

def x_win(ch):
    for i in [0, 1, 2]:
        if table[i][0] == ch and table[i][1] == ch and table[i][2] == ch:
            return True
        if table[0][i] == ch and table[1][i] == ch and table[2][i] == ch:
            return True

    if (table[0][0] == ch and table[1][1] == ch and table[2][2] == ch) or (table[2][0] == ch and table[1][1] == ch and table[0][2] == ch):
        return True

    return False;

def turn_AI():
    rx,ry = -1,-1
    while True :
        rx = random.randint(0,2)
        ry = random.randint(0,2)
        if table[ry][rx] == ".":
            break
    table[ry][rx] = "O"

def retry():
    if messagebox.askquestion("Repeat game", 'retry?') == "yes":
        clear_table()
        canvas.delete('all')
        draw_field_game()
        draw_table
    else:
        sys.exit()

def clear_table():
    for y in [0, 1, 2]:
        for x in [0, 1, 2]:
            table[y][x] = "."

def draw_field_game() :
    canvas.create_line(0, 200, 600, 200, width = 2, fill = 'gray')
    canvas.create_line(0, 400, 600, 400, width = 2, fill = 'gray')
    canvas.create_line(200, 0, 200, 600, width = 2, fill = 'gray')
    canvas.create_line(400, 0, 400, 600, width = 2, fill = 'gray')

def draw_table():
    for y in [0, 1, 2]:
        for x in [0, 1, 2]:
            if table[y][x] == 'X':
                draw_x(x, y)
            if table[y][x] == 'O':
                draw_o(x, y)

def draw_o(x, y):
    canvas.create_oval(x * 200 + 50, y * 200 + 50, x * 200 + 150, y * 200 + 150, width = 5, outline = 'blue')

def draw_x(x, y):
    canvas.create_line(x * 200, y * 200, x * 200 + 200, y * 200 + 200, width = 5, fill = 'red')
    canvas.create_line(x * 200 + 200, y * 200, x * 200 , y * 200 + 200, width = 5, fill = 'red')

gui = Tk(className = "Python Examples - Tic Tac Toe")
canvas = Canvas(gui, width = 600, height = 600)
gui.bind('<Button-1>', click_b1)

# set window size
gui.geometry("600x600+100+100")
gui.resizable(width=False, height=False)
draw_field_game()
canvas.pack()
gui.mainloop()
