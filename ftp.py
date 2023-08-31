from tkinter import *
import random
import time



WIDTH = 1500
HEIGHT = 1000
SPEED = 150
GRAFIC_SIZE = 50 #50, 25, 20, 10, 5, 2, 1
PYTHON_SIZE = 3
PYTHON_COLOR = "#008000"
APPLE_COLOR = "#FF0000"
BACKGROUND_COLOR = "#666666"

SPEED_APPLE = "FFF0F0" #increases speed for a short time
POWER_APPLE = "FFF00F" #increases score and python size by 5
POWER2_APPLE = "FF0000" #increases score and python size by 10



#snake class, an object of snake is created when calling the class#
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


#Food class, an object of food is created when calling the class#
class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH / GRAFIC_SIZE) - 1) * GRAFIC_SIZE
        y = random.randint(0, (HEIGHT / GRAFIC_SIZE) - 1) * GRAFIC_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + GRAFIC_SIZE, y + GRAFIC_SIZE, fill=APPLE_COLOR, tag="apple")


        
#Background = #666666, speed = 150, size = 50, snake = #008000, score<=50#
#place of the dead#
def levelOne():
    pass



def levelTwo():
    pass




def levelThree():
    pass



def levelFour():
    pass



def levelFive():
    pass



def levelSix():
    pass



def levelSeven():
    pass

def updateColor(python, color):
        for i, square in enumerate(python.squares):
            canvas.itemconfig(square, fill=color)
        

def updateSize(size):
    global GRAFIC_SIZE
    GRAFIC_SIZE = size

#calling specific level function depending on score#
def updateGame(score, python):
    global SPEED, levelName

    levelName = "Place Of Death  -  "
    text_label.config(text=levelName)

    if score == 2:
        updateSize(25)
        updateColor(python, "#00800F")
        SPEED = 125
    if score == 5:
        SPEED = 100
    if score == 5:
        SPEED = 90
    if score == 6:
        SPEED = 50


def runSnake(python, x, y):
        python.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + GRAFIC_SIZE, y + GRAFIC_SIZE, fill=PYTHON_COLOR)
        python.squares.insert(0, square)
    


#basically the game, makes the python move#
def nextTurn(python, apple):
    global PYTHON_COLOR
    counter = 0
    
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

        runSnake(python, x, y)

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

            
        
#so you can not move from up to down, right to left, visa verca#
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

                
#checks if franklin is hitting border or himself#
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



#game over, user is able to restart the game#
def gameOver():
    canvas.delete(ALL)
    game.unbind('<Escape>')
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('Arial', 70), text='F', fill="red", tag="f")
    global begin_button
    begin_button = Button(game, text="Restart", font=('Arial', 30), command=restartGame)
    begin_button.place(relx=0.5, rely=0.6, anchor=CENTER)
    global is_paused
    is_paused = False


#when pausing the user is able to continue#
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



#pause function, when pausing the user is able to press on continue or exit#
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


#this function enables the restart, all values are back to stock#
def restartGame():
    global score, direction, SPEED, PYTHON_COLOR, BACKGROUND_COLOR, WIDTH, HEIGHT, GRAFIC_SIZE, PYTHON_SIZE, APPLE_COLOR
    score = 0
    direction = 'right'
    WIDTH = 1500
    HEIGHT = 1000
    SPEED = 150
    GRAFIC_SIZE = 50 #50, 25, 20, 10, 5, 2, 1
    PYTHON_SIZE = 3
    PYTHON_COLOR = "#008000"
    APPLE_COLOR = "#FF0000"
    BACKGROUND_COLOR = "#666666"
    label.config(text="Score:{}".format(score))
    canvas.delete("all")
    global is_paused
    is_paused = False
    beginGame()


#this function start the game and binds the used keys after the user presses begin#
def beginGame():
    global begin_button, isRunning, levelName, label, text_label

    levelName = ""  
    isRunning = False
    canvas.delete(ALL)
    begin_button.destroy()
    customize_button.destroy()


    text_label = Label(top_frame, text=levelName, font=('Arial', 40))
    text_label.pack(side=LEFT)

    label = Label(top_frame, text="Score:{}".format(score), font=('Arial', 40))
    label.pack(side=LEFT)



    game.bind('<Up>', lambda event: changeDirection('up'))
    game.bind('<Down>', lambda event: changeDirection('down'))
    game.bind('<Left>', lambda event: changeDirection('left'))
    game.bind('<Right>', lambda event: changeDirection('right'))
    game.bind('<Escape>', lambda event: pauseGame())

    #global apple
    #python = Snake()
    apple = Food()
    nextTurn(python, apple)


#if pressing exit, the game closes#
def exitGame():
    game.destroy()

isRunning = True
def startIntro():
    global python
    python = Snake()
    if isRunning:
        startScreenIntro(python)
    else:
        beginGame()
    
def startScreenIntro(python):
    global PYTHON_COLOR, direction, x, y

    if isRunning and not is_paused:
        x, y = python.coordinates[0]
        if direction == "up":
            y -= GRAFIC_SIZE
        elif direction == "down":
            y += GRAFIC_SIZE
        elif direction == "right":
            x += GRAFIC_SIZE
        elif direction == "left":
            x -= GRAFIC_SIZE

        if x >= WIDTH - GRAFIC_SIZE and direction == "right":
            direction = "down"
        elif y >= HEIGHT - GRAFIC_SIZE and direction == "down":
            direction = "left"
        elif x <= 0 and direction == "left":
            direction = "up"
        elif y <= 0 and direction == "up":
            direction = "right"
        
        runSnake(python, x, y)


        del python.coordinates[-1]
        canvas.delete(python.squares[-1])
        del python.squares[-1]

    game.after(SPEED, startScreenIntro, python)
    
        


#basically the "main class", setting up the gui#
game = Tk()
game.title("FRANKLIN GAME")
game.resizable(False, False)

score = 0
direction = 'right'
is_paused = False
levelName = ""

top_frame = Frame(game)
top_frame.pack(fill=BOTH)

canvas = Canvas(game, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

begin_button = Button(game, text="Begin", font=('Arial', 30), command=beginGame)
begin_button.place(relx=0.5, rely=0.5, anchor=CENTER)

customize_button = Button(game, text="Customize", font=('Arial', 20))
customize_button.place(relx=0.5, rely=0.6, anchor=CENTER)

startIntro()

game.update()

#center windows
game_width = game.winfo_width()
game_height = game.winfo_height()
screen_width = game.winfo_screenwidth()
screen_height = game.winfo_screenheight()

x = int((screen_width / 2) - (game_width / 2))
y = int((screen_height / 2) - (game_height / 2))

game.geometry(f"{game_width}x{game_height}+{x}+{y}")

game.mainloop()
