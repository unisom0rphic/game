from items.item import Item
from typing import Optional, Callable 

class Weapon(Item):
    def __init__(self, name: str, icon, description: str, 
                 damage: int, use: Optional[Callable] = None) -> None:
        super().__init__(name, icon, description, use)
        self.damage = damage