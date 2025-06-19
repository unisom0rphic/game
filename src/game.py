import pygame
import sys
from utils import constants as const
from utils.functions import load_sprite
from entities.player import Player
from entities.enemy import Enemy
from items.item import Item
from items.weapon import Weapon
from systems.gamefield import GameField
from systems.statusbar import Statusbar
from entities.entity import Direction
from copy import copy

def use_heal_potion(p: Player, *args):  # DAMN this works
    p.health = min(100, p.health + 30)

def equip(p: Player, g: GameField, w: Weapon, *args):
    if p.weapon is not None:
        g.get_tile(p.pos).items.append(p.weapon) 
    p.weapon = w

def load_level(player, game_field, items: dict['Item', tuple[int, int]], 
               wall_img, walls_pos: list[tuple[int, int, Direction, int]], 
               enemies: dict[Enemy, tuple[int, int]]) -> tuple[GameField, list[Enemy]]:
    '''Returns level configuration'''
    game_field.get_tile(player.pos).entity = player

    for enemy, pos in enemies.items():
        enemy.set_pos(pos, game_field) # type: ignore
        game_field.get_tile(pos).entity = enemy
        game_field.get_tile(pos).have_collision = True

    for item, pos in items.items():
        game_field.get_tile(pos).items.append(item)

    for wall in walls_pos:
        game_field.add_wall(wall_img, *wall)

    return game_field, list(enemies.keys())


def handle_input(key, player, enemies, game_field):
    if key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
        
    # Movement
    movements = {
        pygame.K_RIGHT: Direction.EAST,
        pygame.K_d: Direction.EAST,
        pygame.K_LEFT: Direction.WEST,
        pygame.K_a: Direction.WEST,
        pygame.K_UP: Direction.NORTH,
        pygame.K_w: Direction.NORTH,
        pygame.K_DOWN: Direction.SOUTH,
        pygame.K_s: Direction.SOUTH
    }
    
    if key in movements:
        dr, dc = movements[key].value
        new_pos = [player.pos[0] + dr, player.pos[1] + dc]
        if game_field.get_tile(new_pos).entity:
            e = game_field.get_tile(new_pos).entity
            player.attack(e)
        else:
            player.set_pos(new_pos, game_field)
    
    # Item interactions
    elif key == pygame.K_p:
        tile = game_field.get_tile(player.pos)
        if tile.items:
            player.inventory.add_item(tile.items.pop())

    elif key == pygame.K_f:
        slot = player.inventory.selected
        if slot in player.inventory.slots:
            item = player.inventory.slots[slot]
            if item.use:
                item.use(player, game_field, item)
                player.inventory.remove_item(slot)
    
    elif key == pygame.K_g:
        slot = player.inventory.selected
        if slot in player.inventory.slots:
            item = player.inventory.slots[slot]
            game_field.get_tile(player.pos).items.append(item)
            player.inventory.remove_item(slot)
    
    # Inventory selection
    for i, k in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]):
        if k == pygame.K_0:
            slot = 10
        else:
            slot = i + 1
            
        if key == k:
            player.inventory.selected = slot

def main():
    pygame.init()
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("GAME!")
    
    # Load assets
    BLANK_SURF = pygame.Surface((const.TILE_SIZE, const.TILE_SIZE))
    BLANK_SURF.fill(const.BLACK)
    
    INV_SLOT_IMG = load_sprite('Inventory_slot')
    SELECTED_SLOT_IMG = load_sprite('Selected_slot')
    FLOOR_IMG = load_sprite('Floor')
    SWORD_IMG = load_sprite('Sword')
    HEAL_POTION_IMG = load_sprite('HealPotion')
    WALL_IMG = load_sprite('Wall')
    
    FONT = pygame.font.Font(None, 30)
    
    # Create items
    heal_potion = Item('heal_potion', HEAL_POTION_IMG, 'Heals 30 HP', use=use_heal_potion)
    sword = Weapon('Sword', SWORD_IMG, 'A sharp sword', 
                    damage=20, stun_chance=0.4, bleeding_chance=0.3, critical_hit_chance=0.3, 
                    armor_penetration=0.5, use=equip)
    sledgehammer = Weapon('Sledgehammer', BLANK_SURF, 'A really big and heavy sledgehammer', 
                    damage=45, stun_chance=0.8, bleeding_chance=0.2, critical_hit_chance=0.3, 
                    armor_penetration=0.2, use=equip)
    mace = Weapon('Mace', BLANK_SURF, 'A mace', 
                    damage=30, stun_chance=0.5, bleeding_chance=0.2, critical_hit_chance=0.3, 
                    armor_penetration=0.4, use=equip)
    knife = Weapon('Knife', BLANK_SURF, 'A small knife', 
                    damage=10, stun_chance=0.1, bleeding_chance=0.2, critical_hit_chance=0.1, 
                    armor_penetration=0.5, use=equip)
    axe = Weapon('Axe', BLANK_SURF, 'An old axe', 
                    damage=15, stun_chance=0.4, bleeding_chance=0.4, critical_hit_chance=0.5, 
                    armor_penetration=0.4, use=equip)
    
    # Create entities
    player = Player(BLANK_SURF, INV_SLOT_IMG, SELECTED_SLOT_IMG)
    goblin = Enemy('Goblin', health=80, armor=0, dodge_chance=0.5, 
            pos=[0,0], surf=BLANK_SURF, detection_range=10, weapon=knife)
    orc = Enemy('Orc', health=100, armor=10, dodge_chance=0.3, 
            pos=[0,0], surf=BLANK_SURF, detection_range=7, weapon=sword)
    troll = Enemy('Troll', health=120, armor=40, dodge_chance=0.1, 
            pos=[0,0], surf=BLANK_SURF, detection_range=5, weapon=sledgehammer)
    
    
    items_1 = {axe: (4,4), copy(heal_potion): (10, 20), copy(heal_potion): (6, 17), sword: (12, 15)}
    walls_1 = [(7,7,Direction.NORTH,5)]
    enemies_1 = {troll: (12, 14), orc: (11, 2), goblin: (13, 18)}

    # Initialize game systems
    game_field = GameField(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player, game_field, enemies_1)

    _, enemies = load_level(player, game_field, items=items_1, wall_img=WALL_IMG, 
               walls_pos=walls_1, enemies=enemies_1)

    # Initial rendering
    game_field.redraw()
    screen.blit(game_field.display_field(), (0, 0))
    statusbar.update_statusbar()
    pygame.display.update()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_input(event.key, player, enemies, game_field)
                # Apply any existing effects
                player.apply_effects()
                # Enemy AI
                for enemy in enemies:
                    if enemy.health <= 0:
                        enemy.die(game_field)
                        enemies.remove(enemy)
                        del enemy
                    else:
                        enemy.act(player, game_field)
                        enemy.apply_effects()
                
                # Rendering
                game_field.redraw()
                screen.blit(game_field.display_field(), (0, 0))
                statusbar.update_statusbar()
                pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()