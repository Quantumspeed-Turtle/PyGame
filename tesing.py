from tkinter import *
import random

WIDTH = 1500
HEIGHT = 1000
SPEED = 150
GRAFIC_SIZE = 50
PYTHON_SIZE = 3
PYTHON_COLOR = "#0000FF"
APPLE_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = PYTHON_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, PYTHON_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + GRAFIC_SIZE, y + GRAFIC_SIZE, fill=PYTHON_COLOR, tag="python")
            self.squares.append(square)



class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH / GRAFIC_SIZE) - 1) * GRAFIC_SIZE
        y = random.randint(0, (HEIGHT / GRAFIC_SIZE) - 1) * GRAFIC_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + GRAFIC_SIZE, y + GRAFIC_SIZE, fill=APPLE_COLOR, tag="apple")

        

def nextTurn(python, apple):
    global PYTHON_COLOR
    
    if not is_paused:
        x, y = python.coordinates[0]
        if direction == "up":
            y -= GRAFIC_SIZE
        elif direction == "down":
            y += GRAFIC_SIZE
        elif direction == "right":
            x += GRAFIC_SIZE
        elif direction == "left":
            x -= GRAFIC_SIZE

        python.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + GRAFIC_SIZE, y + GRAFIC_SIZE, fill=PYTHON_COLOR)
        python.squares.insert(0, square)

        if x == apple.coordinates[0] and y == apple.coordinates[1]:
            global score
            score += 1
            label.config(text="Score:{}".format(score))
            canvas.delete("apple")
            apple = Food()
        else:
            del python.coordinates[-1]
            canvas.delete(python.squares[-1])
            del python.squares[-1]

        if checkCollision(python):
            gameOver()
        else:
            updateGame(score, python)
            game.after(SPEED, nextTurn, python, apple)

            

def updateGame(score, python):
    global SPEED, PYTHON_COLOR

    if score > 3:
        PYTHON_COLOR = "#00FF00"
        for i, square in enumerate(python.squares):
            canvas.itemconfig(square, fill=PYTHON_COLOR)
        SPEED = 125
    if score > 25:
        SPEED = 100
    if score > 35:
        SPEED = 90
    if score > 50:
        SPEED = 80

        

def changeDirection(update_direction):
    global direction
    if not is_paused:
        if update_direction == 'left':
            if direction != 'right':
                direction = update_direction
        elif update_direction == 'right':
            if direction != 'left':
                direction = update_direction
        elif update_direction == 'up':
            if direction != 'down':
                direction = update_direction
        elif update_direction == 'down':
            if direction != 'up':
                direction = update_direction

                

def checkCollision(python):
    x, y = python.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    if y < 0 or y >= HEIGHT:
        return True

    for body in python.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True

    return False




def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('Arial', 70), text='F', fill="red", tag="f")
    global begin_button
    begin_button = Button(game, text="Restart", font=('Arial', 30), command=restartGame)
    begin_button.place(relx=0.5, rely=0.6, anchor=CENTER)
    global is_paused
    is_paused = False



def continueGame():
    global is_paused, continue_button, exit_button
    is_paused = False
    continue_button.destroy()
    exit_button.destroy()
    canvas.delete("paused")
    # Call nextTurn to continue the game loop
    global python, apple
    nextTurn(python, apple)
    game.bind('<Escape>', lambda event: pauseGame())




def pauseGame():
    global is_paused, continue_button, exit_button
    is_paused = not is_paused
    if is_paused:
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text='PAUSED', font=('Arial', 40), fill="white", tag="paused")
        exit_button = Button(game, text="Exit", font=('Arial', 30), command=exitGame)
        exit_button.place(relx=0.5, rely=0.7, anchor=CENTER)
        continue_button = Button(game, text="Continue", font=('Arial', 30), command=continueGame)
        continue_button.place(relx=0.5, rely=0.6, anchor=CENTER)
        game.unbind('<Escape>')
    else:
        canvas.delete("paused")
        exit_button.destroy()



def exitGame():
    game.destroy()




def restartGame():
    global score, direction, SPEED, PYTHON_COLOR
    score = 0
    direction = 'right'
    SPEED = 150
    PYTHON_COLOR = "#0000FF"
    label.config(text="Score:{}".format(score))
    canvas.delete("all")
    global is_paused
    is_paused = False
    beginGame()





def beginGame():
    global begin_button
    begin_button.destroy()

    game.bind('<Up>', lambda event: changeDirection('up'))
    game.bind('<Down>', lambda event: changeDirection('down'))
    game.bind('<Left>', lambda event: changeDirection('left'))
    game.bind('<Right>', lambda event: changeDirection('right'))
    game.bind('<Escape>', lambda event: pauseGame())

    global python, apple
    python = Snake()
    apple = Food()
    nextTurn(python, apple)




#GUI - Main#
game = Tk()
game.title("PYTHON GAME")
game.resizable(False, False)

score = 0
direction = 'right'
is_paused = False

label = Label(game, text="Score:{}".format(score), font=('Arial', 40))
label.pack()

canvas = Canvas(game, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

begin_button = Button(game, text="Begin", font=('Arial', 30), command=beginGame)
begin_button.place(relx=0.5, rely=0.5, anchor=CENTER)


game.update()

# CENTER THE GAME WINDOW
game_width = game.winfo_width()
game_height = game.winfo_height()
screen_width = game.winfo_screenwidth()
screen_height = game.winfo_screenheight()

x = int((screen_width / 2) - (game_width / 2))
y = int((screen_height / 2) - (game_height / 2))

game.geometry(f"{game_width}x{game_height}+{x}+{y}")

game.mainloop()
