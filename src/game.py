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

def use_potion(p: Player, *args):  # DAMN this works
    p.health = min(100, p.health + 30)

def equip(p: Player, g: GameField, w: Weapon, *args):
    if p.weapon is not None:
        g.get_tile(p.pos).items.append(p.weapon) 
    p.weapon = w

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
        player.set_pos(new_pos, game_field)
    
    # Testing keys
    elif key == pygame.K_v:
        player.health = max(0, player.health - 5)
    elif key == pygame.K_i:
        player.inventory.add_item(sword)
    elif key == pygame.K_o:
        player.inventory.add_item(potion)
    elif key == pygame.K_l:
        for enemy in enemies:
            enemy.act(player, game_field)
    elif key == pygame.K_p:
        tile = game_field.get_tile(player.pos)
        if tile.items:
            player.inventory.add_item(tile.items.pop())
    
    # Inventory selection
    for i, k in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]):
        if k == pygame.K_0:
            slot = 10
        else:
            slot = i + 1
            
        if key == k:
            player.inventory.selected = slot
    
    # Item interactions
    if key == pygame.K_f:
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
    POTION_IMG = load_sprite('Potion')
    WALL_IMG = load_sprite('Wall')
    
    FONT = pygame.font.Font(None, 30)
    
    # Create items
    global sword, potion # FIXME: used for testing, won't be added to the inventory directly anyway 
    potion = Item('Potion', POTION_IMG, 'Heals 30 HP', use=use_potion)
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
    enemies = [
        Enemy('Goblin', 80, 0, [10, 10], BLANK_SURF, detection_range=10, weapon=knife),
        Enemy('Orc', 100, 10, [7, 11], BLANK_SURF, detection_range=7, weapon=sword),
        Enemy('Troll', 120, 40, [0, 15], BLANK_SURF, detection_range=5, weapon=sledgehammer)
    ]
    
    # Initialize game systems
    game_field = GameField(FLOOR_IMG)
    statusbar = Statusbar(screen, FONT, player, game_field, enemies)
    
    # Place entities
    game_field.get_tile(player.pos).entity = player
    for enemy in enemies:
        game_field.get_tile(enemy.pos).entity = enemy
        game_field.get_tile(enemy.pos).have_collision = True
    
    # Place items
    # TODO: battle system x levels (bleeding/armor (isn't efficient against heavy weapons)/defense/dodging maybe/critical hits)
    game_field.get_tile((4,4)).items.append(axe)
    game_field.get_tile((12, 16)).items.append(potion)
    game_field.get_tile((6, 17)).items.append(potion)
    game_field.get_tile((12, 15)).items.append(sword)
    
    # Add walls
    game_field.add_wall(WALL_IMG, 7, 7, Direction.NORTH, 5)

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
                # Enemy AI
                for enemy in enemies:
                    enemy.act(player, game_field)
                
                # Rendering
                game_field.redraw()
                screen.blit(game_field.display_field(), (0, 0))
                statusbar.update_statusbar()
                pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()