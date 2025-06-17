from items.item import Item
from typing import Optional, Callable 

class Weapon(Item):
    def __init__(self, name: str, icon, description: str, 
                 damage: int, stun_chance: float, bleeding_chance: float, critical_hit_chance: float, 
                 armor_penetration: float, use: Optional[Callable] = None) -> None:
        super().__init__(name, icon, description, use)
        self.damage = damage
        self.stun_change = stun_chance
        self.bleeding_chance = bleeding_chance
        self.critical_hit_chance = critical_hit_chance
        self.armor_penetration = armor_penetration
