from entities.entity import Entity
from systems.inventory import Inventory

class Player(Entity):
    def __init__(self, surf, inv_slot_img, selected_slot_img) -> None:
        super().__init__(name='Player', health=100, armor=0, pos=[0, 0], 
                         surf=surf, detection_range=10)
        self.inventory = Inventory(10, inv_slot_img, selected_slot_img)

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

    def get_inv(self) -> Inventory:
        return self.inventory

    @staticmethod
    def manhattan_distance(pos1, pos2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])