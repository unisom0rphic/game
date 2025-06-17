from enum import Enum
from items.weapon import Weapon

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

class Entity:
    def __init__(self, name: str, health: int, armor: int, pos: list[int], 
                 surf, weapon: Weapon, detection_range: int) -> None:
        self.name = name
        self.health = health
        self.armor = armor
        self.pos = pos
        self.surf = surf
        self.weapon = weapon
        self.detection_range = detection_range

    def _attack(self, target: 'Entity') -> None:
        # TODO: needs balance (critical hits/better armor usage)
        target.health -= round(self.weapon.damage / (target.armor/self.weapon.armor_penetration))  

    def stun(self):
        pass

    def bleed(self):
        pass

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

    @staticmethod
    def manhattan_distance(pos1, pos2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])