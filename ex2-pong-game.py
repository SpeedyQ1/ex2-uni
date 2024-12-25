import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 10

# Speeds
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Paddle positions
player1_y = (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2)
player2_y = (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2)

# Ball position
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y

# Scores
player1_score = 0
player2_score = 0

# Fonts
font = pygame.font.Font(None, 36)

def draw():
    """Draw all game elements on the screen."""
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (10, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 20, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw scores
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (SCREEN_WIDTH // 4, 20))
    screen.blit(player2_text, (SCREEN_WIDTH * 3 // 4, 20))

    pygame.display.flip()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key states
    keys = pygame.key.get_pressed()

    # Player 1 movement (W and S keys)
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player1_y += PADDLE_SPEED

    # Player 2 movement (Up and Down arrow keys)
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player2_y += PADDLE_SPEED

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball collision with paddles
    if (ball_x <= 20 and player1_y < ball_y < player1_y + PADDLE_HEIGHT) or \
       (ball_x >= SCREEN_WIDTH - 20 - BALL_SIZE and player2_y < ball_y < player2_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Ball goes out of bounds
    if ball_x < 0:
        player2_score += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_dx *= -1
    if ball_x > SCREEN_WIDTH:
        player1_score += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_dx *= -1

    # Draw everything
    draw()

    # Control frame rate
    clock.tick(60)
