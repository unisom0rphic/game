import pygame
from enum import Enum

TILE_SIZE = 32 
FPS = 60
WIDTH, HEIGHT = 16*TILE_SIZE, 12*TILE_SIZE 
    
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

# Functions
def create_background(background_tile: pygame.Surface) -> pygame.Surface:
    background = pygame.Surface((WIDTH, HEIGHT))
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            background.blit(background_tile, (x,y))
    return background


def render_tile_plain(screen: pygame.Surface, color: pygame.color.Color, x: int, y: int) -> None:
    new_surface = pygame.Surface((TILE_SIZE,TILE_SIZE))
    new_surface.fill(color)
    screen.blit(new_surface, (x*TILE_SIZE, y*TILE_SIZE))


def add_wall(screen: pygame.Surface, color: pygame.color.Color, x: int, y: int, direction: Direction, length: int) -> None:
    match direction:
        case Direction.NORTH:
            if (y-length >= 0):
                [render_tile_plain(screen, color, x, y-i) for i in range(length)]
        case Direction.EAST:
            if (x+length < WIDTH):
                [render_tile_plain(screen, color, x+i, y) for i in range(length)]
        case Direction.SOUTH:
            if (y+length < HEIGHT):
                [render_tile_plain(screen, color, x, y+i) for i in range(length)]
        case Direction.WEST:
            if (x-length >= 0):
                [render_tile_plain(screen, color, x-i, y) for i in range(length)]


def check_collision(surf1: pygame.Surface, surf2: pygame.Surface) -> bool:
    rect1 = surf1.get_rect()
    rect2 = surf2.get_rect()
    if (rect1.x > rect2.x) and (rect1.x < rect2.x+rect2.width) or \
            (rect1.y > rect2.y) and (rect1.y < rect2.y+rect2.height):
            return True
    else:
        return False


def update_statusbar(screen: pygame.Surface, player: Player, font: pygame.font.Font) -> None:
    statusbar = pygame.Surface((WIDTH, 3*TILE_SIZE))
    statusbar_text = font.render(f'Health: {player.health}', False, WHITE)
    statusbar.blit(statusbar_text, (0,0))
    screen.blit(statusbar, (0, HEIGHT-statusbar.get_height()))
    



if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    # Sprites
    FLOOR_IMG = pygame.image.load("sprites/Floor.png").convert_alpha()
    FONT = pygame.font.Font(None, 30)
     
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
                    if (player.pos_x+1 < WIDTH//TILE_SIZE):
                        player.pos_x += 1
                elif event.key == pygame.K_LEFT:
                    if (player.pos_x-1 >= 0):
                        player.pos_x -= 1
                elif event.key == pygame.K_UP:
                    if (player.pos_y-1 >= 0):
                        player.pos_y -= 1
                elif event.key == pygame.K_DOWN:
                    if (player.pos_y+1 < HEIGHT//TILE_SIZE):
                        player.pos_y += 1
                elif event.key == pygame.K_d:
                    if player.health > 5: player.health -= 5


            render_tile_plain(screen, player.player_color, player.pos_x, player.pos_y)
            add_wall(screen, GRAY, x=7, y=7, direction=Direction.NORTH, length=5)
            update_statusbar(screen, player, FONT)

            pygame.display.update()
            clock.tick(FPS)
