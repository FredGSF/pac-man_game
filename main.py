import pygame
import sys
import random

from const import *


class Main:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")

        # Pac-Man starting position and speed
        self.pacman_x, self.pacman_y = WIDTH // 2, HEIGHT // 2
        self.pacman_speed = 5

        # Ghosts
        self.ghosts = [
            {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "speed_x": random.choice([-2, 2]),
                "speed_y": random.choice([-2, 2]),
            }
            for _ in range(3)
        ]

        # Pellets
        self.pellets = [
            {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)}
            for _ in range(20)
        ]

        # Maze
        self.maze = [
            pygame.Rect(50, 50, 700, 20),
            pygame.Rect(50, 50, 20, 700),
            pygame.Rect(50, 750, 700, 20),
            pygame.Rect(750, 50, 20, 720),
            pygame.Rect(150, 150, 500, 20),
            pygame.Rect(150, 150, 20, 300),
            pygame.Rect(150, 400, 500, 20),
            pygame.Rect(650, 150, 20, 270),
            pygame.Rect(250, 250, 300, 20),
            pygame.Rect(250, 250, 20, 150),
            pygame.Rect(450, 250, 20, 150),
            pygame.Rect(250, 400, 220, 20),
            pygame.Rect(450, 400, 100, 20),
            pygame.Rect(350, 350, 20, 50),
            pygame.Rect(350, 350, 50, 20),
            pygame.Rect(450, 350, 50, 20),
            pygame.Rect(550, 250, 20, 150),
            pygame.Rect(550, 400, 100, 20),
            pygame.Rect(50, 650, 700, 20),
            pygame.Rect(50, 550, 700, 20),
        ]

        # Score
        self.score = 0

    def mainloop(self):
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.pacman_x = self.pacman_x
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.pacman_y = self.pacman_y

            # Handle user input
            keys = pygame.key.get_pressed()
            new_pacman_x = (
                self.pacman_x
                + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.pacman_speed
            )
            new_pacman_y = (
                self.pacman_y
                + (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.pacman_speed
            )

            # Check for collisions with maze walls
            pacman_rect = pygame.Rect(
                new_pacman_x - PACMAN_RADIUS,
                new_pacman_y - PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
                2 * PACMAN_RADIUS,
            )
            if all(not pacman_rect.colliderect(wall) for wall in self.maze):
                self.pacman_x, self.pacman_y = new_pacman_x, new_pacman_y

            # Check for collisions with pellets
            for pellet in self.pellets:
                if pygame.Rect(
                    pellet["x"] - PELLET_RADIUS,
                    pellet["y"] - PELLET_RADIUS,
                    2 * PELLET_RADIUS,
                    2 * PELLET_RADIUS,
                ).colliderect(pacman_rect):
                    self.pellets.remove(pellet)
                    self.score += 10

            # Move ghosts
            for ghost in self.ghosts:
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
                ).colliderect(pacman_rect):
                    print("Game Over! Your Score:", self.score)
                    pygame.quit()
                    sys.exit()

            # Clear the screen
            self.screen.fill(BLACK)

            # Draw Maze
            for wall in self.maze:
                pygame.draw.rect(self.screen, WHITE, wall)

            # Draw Pellets
            for pellet in self.pellets:
                pygame.draw.circle(
                    self.screen,
                    WHITE,
                    (round(pellet["x"]), round(pellet["y"])),
                    PELLET_RADIUS,
                )

            # Draw Ghosts
            for ghost in self.ghosts:
                pygame.draw.circle(
                    self.screen,
                    RED,
                    (round(ghost["x"]), round(ghost["y"])),
                    GHOST_RADIUS,
                )

            # Draw Pac-Man
            pygame.draw.circle(
                self.screen,
                YELLOW,
                (round(self.pacman_x), round(self.pacman_y)),
                PACMAN_RADIUS,
            )
            pygame.draw.polygon(
                self.screen,
                BLACK,
                [
                    (round(self.pacman_x), round(self.pacman_y)),
                    (
                        round(self.pacman_x + PACMAN_RADIUS),
                        round(self.pacman_y - PACMAN_RADIUS),
                    ),
                    (
                        round(self.pacman_x + PACMAN_RADIUS),
                        round(self.pacman_y + PACMAN_RADIUS),
                    ),
                ],
            )

            # Display Score
            font = pygame.font.SysFont(None, 36)
            score_text = font.render("Score: " + str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.flip()

            # Control the frames per second
            pygame.time.Clock().tick(60)


# Create an instance of the Main class and start the game loop
if __name__ == "__main__":
    game = Main()
    game.mainloop()
