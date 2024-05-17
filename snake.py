import pygame
import random
import os

# Pygame
pygame.init()

# screen size
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jersey Snake")

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Function to ensure the highscore file is created
def ensure_highscore_file():
    # Get the user's home directory
    home_dir = os.path.expanduser('~')

    # Define the path to the target directory
    target_dir = os.path.join(home_dir, 'Desktop', 'snake-game')

    # Create the directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Define the path to the highscore.txt file
    highscore_path = os.path.join(target_dir, 'high_score.txt')

    # Create the highscore.txt file if it doesn't exist
    if not os.path.exists(highscore_path):
        with open(highscore_path, 'w') as file:
            file.write('0')  # Writing a default high score of 0

    return highscore_path

# Function to read the high score from the file
def read_highscore(file_path):
    with open(file_path, 'r') as file:
        highscore = file.read().strip()
    return int(highscore)

# Function to write a new high score to the file
def write_highscore(file_path, score):
    with open(file_path, 'w') as file:
        file.write(str(score))

# variables
def reset_game():
    global snake_pos, food_pos, direction, score, high_score, high_score_file_path
    snake_pos = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    direction = (0, 0)
    score = 0

    # path for high score txt
    high_score_file_path = ensure_highscore_file()

    # high
    try:
        high_score = read_highscore(high_score_file_path)
    except FileNotFoundError:
        high_score = 0

reset_game()
clock = pygame.time.Clock()

# game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # snake movement
    new_head = (snake_pos[0][0] + direction[0], snake_pos[0][1] + direction[1])

    # eat food
    if new_head == food_pos:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 1
        # Ufor high score updating
        if score > high_score:
            high_score = score
            write_highscore(high_score_file_path, high_score)
    else:
        snake_pos.pop()

    # snake die
    if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake_pos):
        # when the game restarts
        reset_game()
    else:
        snake_pos.insert(0, new_head)

    # the snake shape thingy
    for segment in snake_pos:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # the food
    pygame.draw.rect(screen, RED, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # show the score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(text, (10, 10))

    # show high score
    high_score_text = font.render("High Score: {}".format(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 50))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
