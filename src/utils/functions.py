from math import sqrt
from utils.constants import TILE_SIZE, HEIGHT, STATUSBAR_HEIGHT, WIDTH
import pygame

def load_sprite(img_name: str):
    return pygame.image.load(f'../sprites/{img_name}.png').convert_alpha()

def cartesian_distance(pos1, pos2) -> float:
    r1, c1 = pos1
    r2, c2 = pos2
    return sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)

def manhattan_distance(pos1, pos2) -> int:
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2)

def check_collision(pos1, pos2) -> bool:
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]