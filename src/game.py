import pygame
from enum import Enum

TILE_SIZE = 32 
FPS = 60
WIDTH, HEIGHT = TILE_SIZE*32, TILE_SIZE*24
STATUSBAR_HEIGHT = TILE_SIZE*4

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

    def __init__(self, player_surf):
        self.health = 100
        self.health = 100
        self.armor = 0
        self.inventory = Inventory(10)
        self.pos_x = 0
        self.pos_y = 0
        self.player_color = GRAY 
        self.player_surf = player_surf
        self.player_surf.fill(GRAY)
        print("PLAYER IS CREATED")


class Item:
    def __init__(self, name: str, icon: pygame.Surface, description: str, stackable: bool = True) -> None:
        self.name = name
        self.icon = icon
        self.description = description
        self.stackable = stackable


class Inventory:
    '''
    An inventory class.
    Stackable objects can be stacked indefinetely.
    Unstackable ones can only exist in one instance.   
    '''
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.slots = {}

    def add_item(self, item: Item) -> bool:
        '''Returns True if item can be picked up, False otherwise'''
        if item.name in self.slots:
            if item.stackable:
                item_amount = self.slots[item.name][1] 
                self.slots[item.name] = (item, item_amount + 1) 
                return True
        elif len(self.slots) < self.capacity:
            self.slots[item.name] = (item, 1)
            return True
        return False
            

    def remove_item(self, item: Item) -> bool:
        '''Returns True if item can be deleted, False otherwise'''
        if not item.name in self.slots: return False
        item_amount = self.slots[item.name][1]
        if item_amount <= 0: return False
        self.slots[item.name] = (item, item_amount - 1)
        return True


class InputHandler():
    def __init__(self) -> None:
        pass

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


def check_collision(rect1: pygame.rect.Rect, rect2: pygame.rect.Rect) -> bool:
    if (rect1.x > rect2.x) and (rect1.x < rect2.x+rect2.width) or \
            (rect1.y > rect2.y) and (rect1.y < rect2.y+rect2.height):
            return True
    else:
        return False

class Statusbar():
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, player: Player):
        self.screen = screen
        self.font = font
        self.player = Player

    def update_statusbar(self) -> None:
        statusbar = pygame.Surface((WIDTH, STATUSBAR_HEIGHT))
        statusbar_text = self.font.render(f'Health: {player.health}', False, WHITE)  # lmao multiple line text isn't supported
        statusbar.blit(statusbar_text, (0,0))
        screen.blit(statusbar, (0, HEIGHT-STATUSBAR_HEIGHT))
    



if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    # Sprites
    FLOOR_IMG = pygame.image.load("../sprites/Floor.png").convert_alpha()
    FONT = pygame.font.Font(None, 30)
     
    wall1 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    wall2 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    player = Player(pygame.Surface((TILE_SIZE, TILE_SIZE)))
        
    background = create_background(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player)

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
                    if (player.pos_y+1 < (HEIGHT-STATUSBAR_HEIGHT)//TILE_SIZE):
                        player.pos_y += 1
                elif event.key == pygame.K_d:
                    if player.health > 5: player.health -= 5


            render_tile_plain(screen, player.player_color, player.pos_x, player.pos_y)
            add_wall(screen, GRAY, x=7, y=7, direction=Direction.NORTH, length=5)
            statusbar.update_statusbar()

            pygame.display.update()
            clock.tick(FPS)
