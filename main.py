from tkinter import *
import random

# Constants for game settings
GAME_WIDTH = 1280
GAME_HEIGHT = 720
SPEED = 120
SPACE_SIZE = 80
BODY_PARTS = 3
SNAKE_COLOUR = "#00FFFF"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)
            
class Food:
    
    def __init__(self):
        while True:
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

            if (x, y) not in snake.coordinates:
                break

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")

# Moves Snake based on player input
def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y+= SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    # Updates score if player successfully eats a Food object and increases length of snake
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    # Deletes end of Snake so it stays the same size if Food is not eaten
    else: 
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # Checks to see if Snake has collided with anything
    if check_collisions(snake):
        game_over()
    
    else:
        window.after(SPEED, next_turn, snake, food)

# Changes direction of snake
def change_direction(new_direction):
    
    global direction

    # Check to ensure the input is not directly opposite of the Snake's current direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# Checks to see if Snake has collided with any objects and ends game if true
def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    # Check to see if Snake has collided with the wall
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    
    # Check to see if Snake has collied with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False

# Ends game and prompts Game Over screen
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('comic sans',70), text="GAME OVER", fill="red", tag="gameover")
    
    restart_button = Button(window, text="Restart", command=restart_game, font=('comic sans', 20))
    restart_button.place(x=0, y=0)

# Creates button that resets the game if pressed
def restart_game():
    global snake, food, score, direction, restart_button

    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    next_turn(snake, food)
    restart_button.destroy()

# Creating the game window
window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('comic sans', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2 - (window_width/2)))
y = int((screen_height/2 - (window_height/2)) - 40)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()


