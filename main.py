import pygame
import sys
import random
from pygame.event import custom_type
import pygame_menu 
from pygame_menu import Theme, themes

pygame.init()

FPS = 8
FramePerSec = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 1000

ROWS = 25
COLUMNS = 25

CELL_WIDTH = WIDTH / COLUMNS
CELL_HEIGHT = HEIGHT / ROWS

SNAKE_PINK = (227, 61, 148)
BG_PINK = (255, 213, 250)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(BG_PINK)

direction = "UP"

snake = [{"x": 0, "y": 0}]
playerScore = 0
GAME_STARTED = False
GAME_ENDED = False

custom_pink_theme = Theme(
    background_color=BG_PINK,  
    title_background_color=BG_PINK, 
    title_font_color=(255, 255, 255),  
    title_font_size=50,  
    widget_font=pygame_menu.font.FONT_8BIT, 
    widget_font_color=(50, 50, 50), 
    widget_font_size=50,
    widget_background_color=(255, 228, 225),
    widget_selection_effect=pygame_menu.widgets.HighlightSelection(), 
    widget_padding=(20, 10), 
    widget_border_color=(255, 228, 225),
    widget_border_width=0,  )


def show_outro_scene():
    font = pygame.font.SysFont("8BIT", 60)
    outro_text = font.render(f"Game Over! Score: {playerScore}", True, WHITE)

    DISPLAYSURF.fill(BG_PINK)
    DISPLAYSURF.blit(outro_text, (WIDTH / 2 - outro_text.get_width() / 2, HEIGHT / 3))

    pygame.display.update()


def start_the_game():
    global GAME_STARTED
    GAME_STARTED = True


def mainMenu():
    menu = pygame_menu.Menu("", 600, 400, theme=custom_pink_theme)
    menu.add.button("Play", start_the_game)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    return menu


def initWorld():
    global WORLD
    WORLD = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]


def showWorld():
    DISPLAYSURF.fill(BG_PINK)
    for rowIndex, row in enumerate(WORLD):
        for colIndex, cell in enumerate(row):
            topLeftX, topLeftY = colIndex * CELL_WIDTH, rowIndex * CELL_HEIGHT
            currentColor = BG_PINK
            if cell == 1:
                currentColor = SNAKE_PINK
                pygame.draw.rect(
                    DISPLAYSURF,
                    currentColor,
                    pygame.Rect(topLeftX, topLeftY, CELL_WIDTH, CELL_HEIGHT),
                )
                if rowIndex == snake[0]["y"] and colIndex == snake[0]["x"]:
                    eye_radius = CELL_WIDTH // 8
                    if direction in ["UP", "DOWN"]:
                        eye1_x = topLeftX + CELL_WIDTH // 4
                        eye2_x = topLeftX + 3 * CELL_WIDTH // 4
                        eye_y = topLeftY + (CELL_HEIGHT // 4 if direction == "UP" else 3 * CELL_HEIGHT // 4)
                    else:   
                        eye1_y = topLeftY + CELL_HEIGHT // 4
                        eye2_y = topLeftY + 3 * CELL_HEIGHT // 4
                        eye_x = topLeftX + (CELL_WIDTH // 4 if direction == "LEFT" else 3 * CELL_WIDTH // 4)

                    if direction in ["UP", "DOWN"]:
                        pygame.draw.circle(DISPLAYSURF, BLACK, (eye1_x, eye_y), eye_radius)
                        pygame.draw.circle(DISPLAYSURF, BLACK, (eye2_x, eye_y), eye_radius)
                    else:
                        pygame.draw.circle(DISPLAYSURF, BLACK, (eye_x, eye1_y), eye_radius)
                        pygame.draw.circle(DISPLAYSURF, BLACK, (eye_x, eye2_y), eye_radius)
            elif cell == 2:
                cherry_image = pygame.image.load("khinkali.webp") 
                cherry_image = pygame.transform.scale(
                    cherry_image, (CELL_WIDTH, CELL_HEIGHT)
                )  
                DISPLAYSURF.blit(
                    cherry_image, (topLeftX, topLeftY)
                )



def spawnRandomSnake():
    x = random.randint(0, ROWS - 1)
    y = random.randint(0, COLUMNS - 1)
    snake[0]["x"] = x
    snake[0]["y"] = y


def spawnRandomCherry():
    freePlaces = []
    for rowIndex, row in enumerate(WORLD):
        for colIndex, cell in enumerate(row):
            if cell == 0:
                freePlaces.append((rowIndex, colIndex))
    randomItem = random.randint(0, len(freePlaces) - 1)
    randomItemCoords = freePlaces[randomItem]
    WORLD[randomItemCoords[0]][randomItemCoords[1]] = 2


def handleCherryNAMNAM():
    global playerScore
    playerScore += 1
    print(playerScore)
    spawnRandomCherry()


def snakeDance():
    global snake
    global GAME_ENDED
    previousSnake = [body.copy() for body in snake]

    head = snake[0]
    if direction == "UP":
        head["y"] -= 1
    elif direction == "DOWN":
        head["y"] += 1
    elif direction == "LEFT":
        head["x"] -= 1
    elif direction == "RIGHT":
        head["x"] += 1

    if not (0 <= head["x"] < COLUMNS and 0 <= head["y"] < ROWS):

        GAME_ENDED = True

    for segment in snake[1:]:
        if head["x"] == segment["x"] and head["y"] == segment["y"]:
            GAME_ENDED = True

    hasEaten = False
    if 0 <= head["y"] < ROWS and 0 <= head["x"] < COLUMNS:
        if WORLD[head["y"]][head["x"]] == 2:
            handleCherryNAMNAM()
            hasEaten = True
    for i in range(1, len(snake)):
        snake[i] = previousSnake[i - 1]

    if hasEaten:
        tail = previousSnake[-1]
        snake.append({"x": tail["x"], "y": tail["y"]})

    if not hasEaten:
        tail = previousSnake[-1]
        WORLD[tail["y"]][tail["x"]] = 0

    for segment in snake:
        for segment in snake:
            if 0 <= segment["y"] < ROWS and 0 <= segment["x"] < COLUMNS:
                WORLD[segment["y"]][segment["x"]] = 1


initWorld()
spawnRandomSnake()
spawnRandomCherry()

menu = mainMenu()

last_direction = direction

while True:
    if not GAME_STARTED and not GAME_ENDED:
        DISPLAYSURF.fill(BG_PINK)
        if menu.is_enabled():
            menu.update(pygame.event.get())
            menu.draw(DISPLAYSURF)
        pygame.display.update()
        continue

    if GAME_ENDED:
        break
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and last_direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and last_direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and last_direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and last_direction != "UP":
                direction = "DOWN"

    snakeDance()
    last_direction = direction
    showWorld()

    pygame.display.update()
    FramePerSec.tick(FPS)

while True:
    show_outro_scene()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()
    pygame.display.update()
