import pygame
import random
import os
import sys

# Initialize pygame
pygame.init()

# Set the base path
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Xenzia")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Game variables
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
apple_pos = [random.randrange(1, (WIDTH // 10)) * 10,
             random.randrange(1, (HEIGHT // 10)) * 10]
apple_spawned = True
game_paused = False
game_over = False

# Score and level variables
score = 0
highest_score = 0
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)

# Load background image
background_img = pygame.image.load(os.path.join(base_path, "background.jpg"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load highest score
def load_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

# Save highest score
def save_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))

# Display levels, game manual, and select difficulty
def select_level():
    level_font = pygame.font.Font(None, 48)
    manual_font = pygame.font.Font(None, 32)
    prompt_text = level_font.render("Levels: 1 Easy 2 Medium 3 Hard", True, BLUE)
    manual_text = manual_font.render("Press P Space to pause. Avoid running into yourself!", True, BLUE)
    SCREEN.blit(background_img, (0, 0))
    SCREEN.blit(prompt_text, (WIDTH // 6, HEIGHT // 2))
    SCREEN.blit(manual_text, (WIDTH // 8, HEIGHT // 2 + 50))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 15  # Easy
                elif event.key == pygame.K_2:
                    return 20  # Medium
                elif event.key == pygame.K_3:
                    return 30  # Hard

# Display the pause menu
def pause_menu():
    pause_font = pygame.font.Font(None, 48)
    pause_text = pause_font.render("Game Paused Press R to Restart, Q to Quit, or P to Continue", True, RED)
    SCREEN.blit(pause_text, (WIDTH // 8, HEIGHT // 2))
    pygame.display.flip()
    
    while game_paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return 'restart'
                elif event.key == pygame.K_q:  # Quit the game
                    return 'quit'
                elif event.key in [pygame.K_p, pygame.K_SPACE]:  # Unpause
                    return 'continue'

# Update direction and handle pause
def change_direction(event):
    global snake_direction, game_paused
    if event.key in [pygame.K_p, pygame.K_SPACE]:
        game_paused = not game_paused
    elif not game_paused and not game_over:
        if event.key == pygame.K_UP and snake_direction != 'DOWN':
            snake_direction = 'UP'
        elif event.key == pygame.K_DOWN and snake_direction != 'UP':
            snake_direction = 'DOWN'
        elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

# Move the snake
def move_snake():
    global snake_pos
    head_x, head_y = snake_pos[0]
    if snake_direction == 'UP':
        head_y -= 10
    elif snake_direction == 'DOWN':
        head_y += 10
    elif snake_direction == 'LEFT':
        head_x -= 10
    elif snake_direction == 'RIGHT':
        head_x += 10

    snake_pos.insert(0, [head_x, head_y])

# Display score
def show_score():
    score_text = font.render(f"Score: {score}", True, BLUE)
    high_score_text = font.render(f"High Score: {highest_score}", True, BLUE)
    SCREEN.blit(score_text, [10, 10])
    SCREEN.blit(high_score_text, [10, 40])

# Display Game Over message
def show_game_over():
    game_over_text = game_over_font.render("Game Over", True, RED)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1500)

# Main game loop
def game_loop():
    global apple_pos, apple_spawned, score, snake_pos, highest_score, game_paused, game_over

    # Load the highest score
    highest_score = load_highest_score()
    clock = pygame.time.Clock()

    # Get level from the user
    snake_speed = select_level()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                change_direction(event)

        if game_paused:
            action = pause_menu()
            if action == 'restart':
                score = 0
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                snake_direction = 'RIGHT'
                game_paused = False
            elif action == 'quit':
                pygame.quit()
                sys.exit()
            elif action == 'continue':
                game_paused = False
            continue

        if game_over:
            show_game_over()
            score = 0
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            snake_direction = 'RIGHT'
            game_over = False

        # Move snake
        move_snake()
        
        # Snake goes through walls
        head_x, head_y = snake_pos[0]
        head_x %= WIDTH
        head_y %= HEIGHT
        snake_pos[0] = [head_x, head_y]

        # Check if snake eats apple
        if head_x == apple_pos[0] and head_y == apple_pos[1]:
            apple_spawned = False
            score += 3
            if score > highest_score:
                highest_score = score
                save_highest_score(highest_score)
        else:
            snake_pos.pop()

        # Spawn new apple
        if not apple_spawned:
            apple_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                         random.randrange(1, (HEIGHT // 10)) * 10]
            apple_spawned = True

        # Check for collisions with self
        if snake_pos[0] in snake_pos[1:]:
            game_over = True

        # Update screen
        SCREEN.blit(background_img, (0, 0))
        pygame.draw.circle(SCREEN, RED, (apple_pos[0] + 5, apple_pos[1] + 5), 5)  # Circular apple
        pygame.draw.circle(SCREEN, GREEN, (snake_pos[0][0] + 5, snake_pos[0][1] + 5), 12)  # Larger head
        for i, segment in enumerate(snake_pos[1:], start=1):
            radius = max(5, 10 - i)
            pygame.draw.circle(SCREEN, GREEN, (segment[0] + 5, segment[1] + 5), radius)
        show_score()

        pygame.display.flip()
        clock.tick(snake_speed)

# Start the game loop
if __name__ == "__main__":
    game_loop()
