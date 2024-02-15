import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PACMAN_RADIUS = 30
GHOST_RADIUS = 25
PELLET_RADIUS = 5

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Pac-Man starting position and speed
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_speed = 5

# Ghosts
ghosts = [
    {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed_x": random.choice([-2, 2]),
        "speed_y": random.choice([-2, 2]),
    }
    for _ in range(3)
]

# Pellets
pellets = [
    {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(20)
]

# Score
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle user input
    keys = pygame.key.get_pressed()
    pacman_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * pacman_speed
    pacman_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * pacman_speed

    # Ensure Pac-Man stays within the screen boundaries
    pacman_x = max(PACMAN_RADIUS, min(WIDTH - PACMAN_RADIUS, pacman_x))
    pacman_y = max(PACMAN_RADIUS, min(HEIGHT - PACMAN_RADIUS, pacman_y))

    # Check for collisions with pellets
    for pellet in pellets:
        if pygame.Rect(
            pellet["x"] - PELLET_RADIUS,
            pellet["y"] - PELLET_RADIUS,
            2 * PELLET_RADIUS,
            2 * PELLET_RADIUS,
        ).colliderect(
            pygame.Rect(
                pacman_x - PACMAN_RADIUS,
                pacman_y - PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
            )
        ):
            pellets.remove(pellet)
            score += 10

    # Move ghosts
    for ghost in ghosts:
        ghost["x"] += ghost["speed_x"]
        ghost["y"] += ghost["speed_y"]

        # Bounce off walls
        if ghost["x"] - GHOST_RADIUS < 0 or ghost["x"] + GHOST_RADIUS > WIDTH:
            ghost["speed_x"] *= -1
        if ghost["y"] - GHOST_RADIUS < 0 or ghost["y"] + GHOST_RADIUS > HEIGHT:
            ghost["speed_y"] *= -1

        # Check for collisions with Pac-Man
        if pygame.Rect(
            ghost["x"] - GHOST_RADIUS,
            ghost["y"] - GHOST_RADIUS,
            2 * GHOST_RADIUS,
            2 * GHOST_RADIUS,
        ).colliderect(
            pygame.Rect(
                pacman_x - PACMAN_RADIUS,
                pacman_y - PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
            )
        ):
            print("Game Over! Your Score:", score)
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Draw Pellets
    for pellet in pellets:
        pygame.draw.circle(
            screen, WHITE, (round(pellet["x"]), round(pellet["y"])), PELLET_RADIUS
        )

    # Draw Ghosts
    for ghost in ghosts:
        pygame.draw.circle(
            screen, RED, (round(ghost["x"]), round(ghost["y"])), GHOST_RADIUS
        )

    # Draw Pac-Man
    pygame.draw.circle(
        screen, YELLOW, (round(pacman_x), round(pacman_y)), PACMAN_RADIUS
    )
    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (round(pacman_x), round(pacman_y)),
            (round(pacman_x + PACMAN_RADIUS), round(pacman_y - PACMAN_RADIUS)),
            (round(pacman_x + PACMAN_RADIUS), round(pacman_y + PACMAN_RADIUS)),
        ],
    )

    # Display Score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frames per second
    pygame.time.Clock().tick(60)
