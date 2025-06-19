from entities.entity import Entity
from systems.inventory import Inventory
from items.weapon import Weapon

class Player(Entity):
    def __init__(self, surf, inv_slot_img, selected_slot_img) -> None:
        super().__init__(name='Player', health=100, armor=30, dodge_chance=0.2, pos=[0, 0], 
                         surf=surf, weapon=None, detection_range=10)  # type: ignore
        self.inventory = Inventory(10, inv_slot_img, selected_slot_img)

    def attack(self, target) -> None:
        self._attack(target)

    def get_info(self) -> dict:
        return {
            "health": self.health,
            "armor": self.armor,
            "pos": self.pos
        }

    def get_env_info(self, game_field, enemies) -> dict:
        env_info = {}
        current_tile = game_field.get_tile(self.pos)
        items_around = [item.name for item in current_tile.items]
        
        enemies_around = [
            enemy.name for enemy in enemies 
            if self.manhattan_distance(self.pos, enemy.pos) <= self.detection_range
        ]
        
        if items_around:
            env_info['items_around'] = items_around[:3]
        if enemies_around:
            env_info['enemies_around'] = enemies_around[:3]
        
        return env_info

    def list_effects(self) -> dict:
        effects = []
        if self.bleeding_time > 0:
            effects.append('bleeding')
        if self.stun_time > 0:
            effects.append('stunned') 

        return {"Effects": effects} if effects else {}

    def get_inv(self) -> Inventory:
        return self.inventory
