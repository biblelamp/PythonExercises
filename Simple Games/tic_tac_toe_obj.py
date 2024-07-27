from tkinter import *
from tkinter import messagebox
import random
import sys
from table_obj import *

game_tbl = table_obj()
ini_file = 'tic_tac_toe.txt'

def draw_line(canvas) :
    canvas.create_line(0, 200, 600, 200, width = 2, fill = 'gray')
    canvas.create_line(0, 400, 600, 400, width = 2, fill = 'gray')
    canvas.create_line(200, 0, 200, 600, width = 2, fill = 'gray')
    canvas.create_line(400, 0, 400, 600, width = 2, fill = 'gray')

def click_b1(event):
    x = event.x
    y = event.y
    int_x = int(x / 200)
    int_y = int(y / 200)
    s = "Mouse click x={} y={}".format(int_x, int_y)
    gui.title(s)
    if game_tbl.get(int_y, int_x) == ".":
        game_tbl.set(int_y, int_x, "X")
        game_tbl.draw(canvas)
        if not game_tbl.is_win("X") :
            if not game_tbl.is_full():
                turn_AI()
                game_tbl.draw(canvas)
                game_tbl.save(ini_file)
                game_tbl.read_file(ini_file)
                if game_tbl.is_win("O"):
                    messagebox.showinfo("Information", "You lose")
                    retry()

            else:
                messagebox.showinfo("Information", "Draw")
                retry()

        else:
            messagebox.showinfo("Information", "You win")
            retry()

def turn_AI():
    rx,ry = -1,-1
    while True :
        rx = random.randint(0, 2)
        ry = random.randint(0, 2)
        if game_tbl.get(ry,rx) == ".":
            break
    game_tbl.set(ry, rx, "O")

def retry():
    if messagebox.askquestion("Repeat game", 'retry?') == "yes":
        game_tbl.clear()
        canvas.delete('all')
        draw_line(canvas)
        game_tbl.draw(canvas)
    else:
        sys.exit()

gui = Tk(className = "Python Examples - Tic Tac Toe")
canvas = Canvas(gui, width = 600, height = 600)
gui.bind('<Button-1>', click_b1)

# set window size
gui.geometry("600x600+100+100")
gui.resizable(width=False, height=False)
draw_line(canvas)
game_tbl.read_file(ini_file)
game_tbl.draw(canvas)
canvas.pack()
gui.mainloop()