import pygame
import numpy as np
from enum import Enum
from typing import Callable

TILE_SIZE = 32 
FPS = 30
WIDTH, HEIGHT = TILE_SIZE*30, TILE_SIZE*25
STATUSBAR_HEIGHT = TILE_SIZE*5
LINE_OFFSET = 20 # px

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
    def __init__(self, player_surf: pygame.Surface) -> None:
        self.health = 100
        self.armor = 0
        self.inventory = Inventory(10)
        self.pos_x = 0
        self.pos_y = 0
        self.player_color = GRAY 
        self.player_surf = player_surf
        self.player_surf.fill(GRAY)
        print("PLAYER IS CREATED")

    def get_info(self) -> dict:
        '''Returns info about the player in a dictionary'''
        return {"health": self.health, 
                "armor": self.armor, 
                "slots": self.inventory.slots,
                "position": (self.pos_x, self.pos_y)}


class Tile:
    def __init__(self, image: pygame.Surface, position: tuple) -> None:
        self.image = image
        self.position = position


class GameField:
    def __init__(self, background_image: pygame.Surface) -> None:
        self.tiles = np.array([[Tile(background_image, (i, j))
                        for i in range(WIDTH//TILE_SIZE)] 
                        for j in range((HEIGHT-STATUSBAR_HEIGHT)//TILE_SIZE)])  # np.array as an optimization attempt
        print(f'GameField tiles shape: {self.tiles.shape}')
        self.field_surf = pygame.Surface((WIDTH, HEIGHT))
        self._redraw()

    def _redraw(self) -> None:
        self.field_surf.fill(BLACK)
        for row in self.tiles:
            for tile in row:
                self.field_surf.blit(tile.image, (tile.position[0]*TILE_SIZE, tile.position[1]*TILE_SIZE))

    def _swap(self, pos1: tuple, pos2: tuple) -> None:
        x1, y1 = pos1
        x2, y2 = pos2
        self.tiles[x1,y1], self.tiles[x2,y2] = self.tiles[x2,y2], self.tiles[x1,y1]

    def change_tile(self, tile: Tile) -> None:
        x, y = tile.position
        self.tiles[x,y] = tile

    def display_field(self) -> pygame.Surface:
        return self.field_surf




class Item:
    def __init__(self, name: str, icon: pygame.Surface, description: str, 
                 use: Callable[..., bool] | None, stackable: bool = True) -> None:
        self.name = name
        self.icon = icon
        self.description = description
        self.stackable = stackable
        self.use = use


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


class Statusbar():
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, player: Player):
        self.screen = screen
        self.font = font
        self.player = player

    def update_statusbar(self) -> None:
        statusbar = pygame.Surface((WIDTH, STATUSBAR_HEIGHT))
        player_info = player.get_info()
        statusbar_text = []
        for feature, value in player_info.items():
            statusbar_text.append(f'{feature}: {value}')
        for i, feature in enumerate(statusbar_text):
            feature_surf = FONT.render(feature, False, WHITE)
            statusbar.blit(feature_surf, (0, i*LINE_OFFSET))
        screen.blit(statusbar, (0, HEIGHT-STATUSBAR_HEIGHT))

# Functions
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






if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    # Sprites
    blank_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blank_surf.fill(WHITE)  # for testing purposes
    FLOOR_IMG = pygame.image.load("../sprites/Floor.png").convert_alpha()
    FONT = pygame.font.Font(None, 30)

    # Items
    sword = Item('Sword', blank_surf, 'A sword', None, False)
     
    wall1 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    wall2 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    player = Player(pygame.Surface((TILE_SIZE, TILE_SIZE)))
        
    game_field = GameField(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player)

    # game loop
    running = True
    while running:
        screen.blit(game_field.display_field(), (0,0))

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
                elif event.key == pygame.K_i:
                    player.inventory.add_item(sword)


            render_tile_plain(screen, player.player_color, player.pos_x, player.pos_y)
            add_wall(screen, GRAY, x=7, y=7, direction=Direction.NORTH, length=5)
            statusbar.update_statusbar()

            pygame.display.update()
            clock.tick(FPS)
