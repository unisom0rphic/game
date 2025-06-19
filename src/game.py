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

def use_armor_potion(p: Player, *args):  # DAMN this works
    p.armor = min(100, p.armor + 30)

def equip(p: Player, g: GameField, w: Weapon, *args):
    if p.weapon is not None:
        g.get_tile(p.pos).items.append(p.weapon) 
    p.weapon = w

def load_level(player, game_field, statusbar, items: dict['Item', tuple[int, int]], 
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

    enemies_list = list(enemies.keys())
    statusbar.enemies = enemies_list

    return game_field, enemies_list


def handle_input(key, player, enemies, game_field):
        
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
        if (0 <= new_pos[0] < game_field.height) and (0 <= new_pos[1] < game_field.width):
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
    
    PLAYER_IMG = load_sprite('Player')
    INV_SLOT_IMG = load_sprite('Inventory_slot')
    SELECTED_SLOT_IMG = load_sprite('Selected_slot')
    FLOOR_IMG = load_sprite('Floor')
    SWORD_IMG = load_sprite('Sword')
    KNIFE_IMG = load_sprite('Knife')
    AXE_IMG = load_sprite('Axe')
    SLEDGEHAMMER_IMG = load_sprite('Sledgehammer')
    HEAL_POTION_IMG = load_sprite('HealPotion')
    ARMOR_POTION_IMG = load_sprite('ArmorPotion')
    WALL_IMG = load_sprite('Wall')

    
    FONT = pygame.font.Font(None, 30)
    
    # Create items
    heal_potion = Item('Heal potion', HEAL_POTION_IMG, 'Heals 30 HP', use=use_heal_potion)
    armor_potion = Item('Armor potion', ARMOR_POTION_IMG, 'Adds 30 armor points', use=use_armor_potion)
    sword = Weapon('Sword', SWORD_IMG, 'A sharp sword', 
                    damage=15, stun_chance=0.2, bleeding_chance=0.2, critical_hit_chance=0.3, 
                    armor_penetration=0.5, use=equip)
    sledgehammer = Weapon('Sledgehammer', SLEDGEHAMMER_IMG, 'A really big and heavy sledgehammer', 
                    damage=45, stun_chance=0.6, bleeding_chance=0.1, critical_hit_chance=0.3, 
                    armor_penetration=0.2, use=equip)
    mace = Weapon('Mace', BLANK_SURF, 'A mace', 
                    damage=30, stun_chance=0.4, bleeding_chance=0.1, critical_hit_chance=0.3, 
                    armor_penetration=0.4, use=equip)
    knife = Weapon('Knife', KNIFE_IMG, 'A small knife', 
                    damage=10, stun_chance=0.1, bleeding_chance=0.2, critical_hit_chance=0.1, 
                    armor_penetration=0.5, use=equip)
    axe = Weapon('Axe', AXE_IMG, 'An old axe', 
                    damage=15, stun_chance=0.2, bleeding_chance=0.4, critical_hit_chance=0.5, 
                    armor_penetration=0.4, use=equip)
    
    # Create entities
    player = Player(PLAYER_IMG, INV_SLOT_IMG, SELECTED_SLOT_IMG)
    goblin = Enemy('Goblin', health=40, armor=0, dodge_chance=0.5, 
            pos=[0,0], surf=BLANK_SURF, detection_range=10, weapon=knife)
    orc = Enemy('Orc', health=60, armor=10, dodge_chance=0.3, 
            pos=[0,0], surf=BLANK_SURF, detection_range=7, weapon=sword)
    troll = Enemy('Troll', health=80, armor=40, dodge_chance=0.1, 
            pos=[0,0], surf=BLANK_SURF, detection_range=5, weapon=sledgehammer)
    
    
    items_1 = {axe: (4,4), copy(heal_potion): (10, 20), copy(heal_potion): (6, 17), copy(armor_potion): (13, 8), sword: (12, 15), 
               copy(heal_potion): (16, 19), copy(sledgehammer): (14, 22), copy(armor_potion): (15, 23)}
    walls_1 = [(9,7,Direction.NORTH,7), (10,5,Direction.EAST,9), (5,15,Direction.SOUTH,11), (3,18,Direction.EAST,9),
               (17,9,Direction.EAST,15), (14,20,Direction.NORTH,9)]
    enemies_1 = {copy(troll): (12, 14), copy(orc): (11, 2), copy(goblin): (13, 18)}

    items_2 = {copy(knife): (3, 10)}
    walls_2 = [(3,3,Direction.SOUTH,9)]
    enemies_2 = {troll: (9, 1)}

    # Initialize game systems
    game_field = GameField(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player, game_field, enemies=None)

    # _, enemies = load_level(player, game_field, items=items_1, wall_img=WALL_IMG, 
    #            walls_pos=walls_1, enemies=enemies_1)
    _, enemies = load_level(player, game_field, statusbar, items=items_1, wall_img=WALL_IMG, 
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
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if player.health <= 0:
                    statusbar.dead_message()
                else:
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

                player.health = max(0,player.health)
                
                # Rendering
                game_field.redraw()
                screen.blit(game_field.display_field(), (0, 0))
                statusbar.update_statusbar()
                pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()