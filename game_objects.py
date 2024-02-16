import pygame
import random
from const import *


def create_pellets(num_pellets):
    pellets = [
        {"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)}
        for _ in range(num_pellets)
    ]
    return pellets


def create_ghosts(num_ghosts):
    ghosts = [
        {
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "speed_x": random.choice([-2, 2]),
            "speed_y": random.choice([-2, 2]),
        }
        for _ in range(num_ghosts)
    ]
    return ghosts
