import pygame
import numpy as np
from enum import Enum
from typing import Callable, Optional


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
        self.inventory = Inventory(10, INV_SLOT_IMG)
        self.pos = [0,0]
        self.player_color = GRAY 
        self.player_surf = player_surf
        self.player_surf.fill(GRAY)
        print("PLAYER IS CREATED")

    def get_info(self) -> dict:
        '''Returns info about the player in a dictionary'''
        return {"health": self.health, 
                "armor": self.armor, 
                "position": self.pos}

    def get_inv(self) -> 'Inventory':
        return self.inventory


class Tile:
    def __init__(self, image: pygame.Surface, position: tuple, have_collision: bool = False) -> None:
        self.image = image
        self.position = position
        self.have_collision = have_collision


class GameField:
    def __init__(self, background_image: pygame.Surface) -> None:
        self.tiles = np.array([[Tile(background_image, (r, c))
                        for c in range(WIDTH//TILE_SIZE)]
                        for r in range((HEIGHT-STATUSBAR_HEIGHT)//TILE_SIZE)])  # np.array as an optimization attempt
        print(f'GameField tiles shape: {self.tiles.shape}')
        self.field_surf = pygame.Surface((WIDTH, HEIGHT))
        self._redraw()

    def _redraw(self) -> None:
        self.field_surf.fill(BLACK)
        for line in self.tiles:
            for tile in line:
                row, col = tile.position
                self.field_surf.blit(tile.image, (col*TILE_SIZE, row*TILE_SIZE))

    def _swap(self, pos1: tuple, pos2: tuple) -> None:
        r1, c1 = pos1
        r2, c2 = pos2
        self.tiles[r1,c1], self.tiles[r2,c2] = self.tiles[r2,c2], self.tiles[r1,c1]
        self._redraw()

    def change_tile(self, tile: Tile) -> None:
        r, c = tile.position
        self.tiles[r,c] = tile
        self._redraw()

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
    def __init__(self, capacity: int, empty_slot: pygame.Surface) -> None:
        self.capacity = capacity
        self.slots = {}
        self.INV_SLOT_IMG = empty_slot

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
        self.statusbar = pygame.Surface((WIDTH, STATUSBAR_HEIGHT))
        self.PANEL_SECTION_OFFSET = WIDTH//3

    def update_statusbar(self) -> None:
        self.statusbar.fill(BLACK)
        self._update_right_panel()  # general info
        self._update_middle_panel()  # inventory
        self._update_left_panel()  # environment
        screen.blit(self.statusbar, (0, HEIGHT-STATUSBAR_HEIGHT))

    def _update_right_panel(self) -> None:
        right_panel_text = []
        player_info = player.get_info()
        for feature, value in player_info.items():
            right_panel_text.append(f'{feature}: {value}')
        for i, feature in enumerate(right_panel_text):
            feature_surf = FONT.render(feature, False, WHITE)
            self.statusbar.blit(feature_surf, (0, i*LINE_OFFSET))

    def _update_middle_panel(self) -> None:
        inv = player.get_inv()
        inv_slots = list(inv.slots.values())
        icons_in_line = inv.capacity//2
        middle_panel_surf = pygame.Surface((TILE_SIZE*icons_in_line, TILE_SIZE*2))
        for i in range(inv.capacity):
            is_empty = i >= len(inv_slots)
            is_in_second_line = i >= icons_in_line
            # slot is a tuple, containing an item and it's amount
            item = inv_slots[i][0] if not is_empty else None
            index_in_line = i-is_in_second_line*icons_in_line
            icon_pos = TILE_SIZE*index_in_line,TILE_SIZE*is_in_second_line
            if item != None:
                middle_panel_surf.blit(item.icon, (icon_pos))
                middle_panel_surf.blit(inv.INV_SLOT_IMG, (icon_pos))
            else:
                middle_panel_surf.blit(BLANK_SURF, (icon_pos))
                middle_panel_surf.blit(inv.INV_SLOT_IMG, (icon_pos))
        self.statusbar.blit(middle_panel_surf, (self.PANEL_SECTION_OFFSET, 0))

    def _update_left_panel(self) -> None:
        left_panel_text = []
        env_surf = pygame.Surface((self.PANEL_SECTION_OFFSET, STATUSBAR_HEIGHT))
        # env_info = player.get_env_info()
        self.statusbar.blit(env_surf, (self.PANEL_SECTION_OFFSET*2, 0))

# Functions
def render_tile_plain(screen: pygame.Surface, color: pygame.color.Color, pos: list[int]) -> None:
    new_surface = pygame.Surface((TILE_SIZE,TILE_SIZE))
    new_surface.fill(color)
    screen.blit(new_surface, (pos[1]*TILE_SIZE, pos[0]*TILE_SIZE))

def add_wall(screen: pygame.Surface, wall_img: pygame.Surface, gamefield: GameField, row: int, col: int, direction: Direction, length: int) -> None:
    match direction:
        case Direction.NORTH:
            if (row-length >= 0):
                for i in range(length):
                    wall = Tile(wall_img, (row-i,col), True)
                    gamefield.change_tile(wall)
        case Direction.EAST:
            if (col+length < WIDTH):
                for i in range(length):
                    wall = Tile(wall_img, (row-i,col), True)
                    gamefield.change_tile(wall)
        case Direction.SOUTH:
            if (row+length < HEIGHT):
                for i in range(length):
                    wall = Tile(wall_img, (row+i, col), True)
                    gamefield.change_tile(wall)
        case Direction.WEST:
            if (col-length >= 0):
                for i in range(length):
                    wall = Tile(wall_img, (row, col-i), True)
                    gamefield.change_tile(wall)

def check_collision(pos1: list[int], pos2: list[int]) -> bool:
    return (pos1[0] == pos2[0] and pos1[1] == pos2[1])

def load_sprite(img_name: str) -> pygame.Surface:
    return pygame.image.load(f'../sprites/{img_name}.png').convert_alpha()



if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    # Sprites
    BLANK_SURF = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert_alpha()
    BLANK_SURF.fill(BLACK)

    INV_SLOT_IMG = load_sprite('Inventory_slot')
    FLOOR_IMG    = load_sprite('Floor')
    SWORD_IMG    = load_sprite('Sword')
    POTION_IMG   = load_sprite('Potion')
    FONT = pygame.font.Font(None, 30)

    # Items
    sword = Item('Sword', SWORD_IMG, 'A sword', None, False)
    potion = Item('Potion', POTION_IMG, 'A potion', None)
     
    wall1 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    wall2 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    player = Player(pygame.Surface((TILE_SIZE, TILE_SIZE)))
        
    game_field = GameField(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player)

    # game loop
    running = True
    while running:
        screen.blit(game_field.display_field(), (0,0))

        render_tile_plain(screen, player.player_color, player.pos)
        add_wall(screen, BLANK_SURF, game_field, 7, 7, direction=Direction.NORTH, length=5)
        statusbar.update_statusbar()

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RIGHT:
                    next_pos = [player.pos[0], player.pos[1]+1]
                    if (next_pos[1] < WIDTH//TILE_SIZE):
                        is_solid = game_field.tiles[next_pos[0]][next_pos[1]].have_collision
                        if not is_solid:
                            player.pos = next_pos
                elif event.key == pygame.K_LEFT:
                    next_pos = [player.pos[0], player.pos[1] - 1]
                    is_solid = game_field.tiles[next_pos[0]][next_pos[1]].have_collision
                    if (next_pos[1] >= 0) and not is_solid:
                        player.pos = next_pos
                elif event.key == pygame.K_UP:
                    next_pos = [player.pos[0]-1, player.pos[1]]
                    is_solid = game_field.tiles[next_pos[0]][next_pos[1]].have_collision
                    if (next_pos[0] >= 0) and not is_solid:
                        player.pos = next_pos
                elif event.key == pygame.K_DOWN:
                    next_pos = [player.pos[0]+1, player.pos[1]]
                    is_solid = game_field.tiles[next_pos[0]][next_pos[1]].have_collision
                    if (next_pos[0] < (HEIGHT-STATUSBAR_HEIGHT)//TILE_SIZE) and not is_solid:
                        player.pos = next_pos
                elif event.key == pygame.K_d:
                    if player.health > 5: player.health -= 5
                elif event.key == pygame.K_i:
                    player.inventory.add_item(sword)
                elif event.key == pygame.K_o:
                    player.inventory.add_item(potion)

