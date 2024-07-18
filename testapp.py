from tkinter import *
import random

# constants for the game
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Class for the game
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake"
            )
            self.squares.append(square)

        print(f"Snake initialized with coordinates: {self.coordinates}")

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food"
        )

        print(f"Food created at coordinates: {self.coordinates}")

# functions definition
def next_turn(snake, food):
    if game_running and not paused:
        x, y = snake.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        snake.coordinates.insert(0, (x, y))

        square = canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )

        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            label.config(text="Score:{}".format(score))
            canvas.delete("food")
            food = Food()
        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if check_collision(snake):
            game_over()
        else:
            window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global game_running
    game_running = False
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text="GAME OVER",
        fill="red",
        tags="game",
    )
    restart_button.pack()

def start_game(event=None):
    global game_running, score, direction, snake, food, paused
    if not game_running:
        game_running = True
        paused = False
        score = 0
        direction = 'down'
        label.config(text="Score: {}".format(score))
        canvas.delete(ALL)
        snake = Snake()
        food = Food()
        window.bind('<Left>', lambda event: change_direction('left'))
        window.bind('<Right>', lambda event: change_direction('right'))
        window.bind('<Up>', lambda event: change_direction('up'))
        window.bind('<Down>', lambda event: change_direction('down'))
        window.bind('<space>', toggle_pause)
        start_label.pack_forget()
        restart_button.pack_forget()
        next_turn(snake, food)

def toggle_pause(event=None):
    global paused
    paused = not paused

def show_start_screen():
    global start_label
    start_label = Label(window, text="Press 'Enter' to Start", font=("consolas", 40))
    start_label.pack()
    window.bind('<Return>', start_game)

def restart_game():
    global start_label, restart_button
    start_label.pack_forget()
    restart_button.pack_forget()
    show_start_screen()

# creating a window for game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# creating score window
score = 0
direction = 'down'
paused = False
game_running = False

# setting up score card above
label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

# setting up canvas for game
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# centralizing the game window when it opens
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_height / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Show start screen
show_start_screen()

restart_button = Button(window, text="Restart Game", font=("consolas", 20), command=restart_game)

window.mainloop()
