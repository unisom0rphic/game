import pygame
from enum import Enum

WIDTH, HEIGHT = 800, 640 
TILE_SIZE = 32 
FPS = 60
    
# Colors
WHITE = pygame.color.Color(255,255,255)
BLACK = pygame.color.Color(0,0,0)
GRAY = pygame.color.Color(100, 100, 100)


# Directions
class Direction(Enum):
    NORTH = 1
    EAST  = 2
    SOUTH = 3
    WEST  = 4

# Classes
class Player:
    health = 100
    armor = 0
    pos_x = 0
    pos_y = 0
    player_color = GRAY 
    player_rect = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    def __init__(self):
        self.health = 100
        print("PLAYER IS CREATED")

def create_background(background_tile: pygame.Surface) -> pygame.Surface:
    background = pygame.Surface((WIDTH, HEIGHT))
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            background.blit(background_tile, (x,y))

    return background


# Functions
def render_tile_rect(screen: pygame.Surface, color: pygame.color.Color, x: int, y: int) -> None:
    new_surface = pygame.Surface((TILE_SIZE,TILE_SIZE))
    new_surface.fill(color)
    screen.blit(new_surface, (x*TILE_SIZE, y*TILE_SIZE))

def render_tile():
    pass

# TODO: add collision function
def check_collision():
    pass

# TODO: add other directions (north works fine for now), add bounds check
def add_wall(screen: pygame.Surface, color: pygame.color.Color, x: int, y: int, direction: Direction, length: int) -> None:
    match direction:
        case Direction.NORTH:
           [render_tile_rect(screen, color, x, y+i) for i in range(length)]
        case Direction.EAST:
            pass
        case Direction.SOUTH:
            pass
        case Direction.WEST:
            pass




if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    # Sprites
    FLOOR_IMG = pygame.image.load("sprites/Floor.png").convert_alpha()
     
    wall1 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    wall2 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    player = Player()

    background = create_background(FLOOR_IMG)

    # game loop
    running = True
    while running:
        screen.blit(background, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RIGHT:
                    player.pos_x += 1
                elif event.key == pygame.K_LEFT:
                    player.pos_x -= 1
                elif event.key == pygame.K_UP:
                    player.pos_y -= 1
                elif event.key == pygame.K_DOWN:
                    player.pos_y += 1


            render_tile_rect(screen, player.player_color, player.pos_x, player.pos_y)
            add_wall(screen, GRAY, 7, 7, Direction.NORTH, 5)
            # render_tile_rect(screen, GRAY, 5, 6)
            # render_tile_rect(screen, GRAY, 5, 7)

            pygame.display.update()
            clock.tick(FPS)
