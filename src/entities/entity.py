from enum import Enum
from items.weapon import Weapon
from utils.constants import BLEEDING_DAMAGE, STUN_TIME, BLEEDING_TIME
from random import random

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

class Entity:
    def __init__(self, name: str, health: int, armor: int, dodge_chance: float, pos: list[int], 
                 surf, weapon: Weapon, detection_range: int) -> None:
        self.name = name
        self.health = health
        self.armor = armor
        self.pos = pos
        self.surf = surf
        self.weapon = weapon
        self.detection_range = detection_range
        self.dodge_chance = dodge_chance
        # Combat 
        self.stun_time = 0
        self.bleeding_time = 0
        self.stunned = False  # only influences the ability to attack


    def _attack(self, target: 'Entity') -> None:
        if self.stunned:
            return

        if self.weapon is None:
            return

        target_did_dodge = random() < target.dodge_chance
        if target_did_dodge:
            print(f'{self.name}: dodged')
            return

        damage = self.weapon.damage
        armor = target.armor
        penetration = self.weapon.armor_penetration

        is_critical = random() < self.weapon.critical_hit_chance
        if is_critical:
            print(f'{self.name}: critical')
            damage *= 1.5

        is_stunning = random() < self.weapon.stun_chance
        if is_stunning:
            target.stun_time = STUN_TIME
            target.stunned = True

        is_bleedy = random() < self.weapon.bleeding_chance
        if is_bleedy:
            target.bleeding_time += BLEEDING_TIME

        if armor > penetration:
            armor_damage = damage*(1 - penetration)
            target.armor = max(0, target.armor-armor_damage)
            target.health -= damage*penetration//3  # so lower penetration does less damage

        else:
            target.health -= damage

    def set_pos(self, direction: Direction | tuple[int], game_field) -> None:
        if isinstance(direction, Direction):
            next_pos = direction.value
        else:
            next_pos = direction

        if (0 <= next_pos[0] < game_field.height and 
            0 <= next_pos[1] < game_field.width): # type: ignore
            tile = game_field.get_tile(next_pos)
            if not tile.have_collision:
                current_tile = game_field.get_tile(self.pos)
                current_tile.entity = None
                current_tile.have_collision = False
                
                self.pos = list(next_pos)
                new_tile = game_field.get_tile(self.pos)
                new_tile.entity = self
                new_tile.have_collision = True

    def apply_effects(self) -> None:
        if self.bleeding_time > 0:
            self.bleeding_time -= 1
            self.health -= BLEEDING_DAMAGE
        if self.stun_time > 0:
            self.stun_time -= 1
            self.stunned = True
        else:
            self.stunned = False


    @staticmethod
    def manhattan_distance(pos1, pos2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])