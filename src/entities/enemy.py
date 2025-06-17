from entities.entity import Entity, Direction
from utils.functions import manhattan_distance
from random import choice, randint
from items.weapon import Weapon

class Enemy(Entity):
    def __init__(self, name: str, health: int, armor: int, pos: list[int], 
                 surf, weapon: Weapon, detection_range: int) -> None:
        super().__init__(name, health, armor, pos, surf, weapon, detection_range)
        self._path = None
        self.weapon = weapon
        self._idle_state_wait_time = randint(1, 3)

    def act(self, target: Entity, game_field) -> None:
        if self.visual_contact(target, game_field):
            dist = manhattan_distance(self.pos, target.pos)
            if dist == 1:
                self._attack(target)
            else:
                self.move_towards(target, game_field)
        else:
            if self._idle_state_wait_time:
                self._idle_state_wait_time -= 1
            else:
                self._move_idle(game_field)
                self._idle_state_wait_time = randint(1,3)

    def visual_contact(self, target: Entity, game_field) -> bool:
        if manhattan_distance(self.pos, target.pos) > self.detection_range:
            return False

        r, c = self.pos
        tr, tc = target.pos
        while (r, c) != (tr, tc):
            dr = 1 if r < tr else -1 if r > tr else 0
            dc = 1 if c < tc else -1 if c > tc else 0
            r += dr
            c += dc
            tile = game_field.get_tile((r, c))
            if tile.have_collision and tile.entity is None:
                return False
        return True

    def move_towards(self, target: Entity, game_field) -> None:
        if self._path:
            next_pos = self._path.pop(0)
            self.set_pos(next_pos, game_field)
        elif self.visual_contact(target, game_field):
            self._update_path(target, game_field)

    def _move_idle(self, game_field):
        d = choice(list(Direction))
        r, c = self.pos
        next_pos = r+d.value[0], c+d.value[1]
        tile = game_field.get_tile(next_pos)
        if not tile.have_collision and tile.entity is None:
            self.set_pos(next_pos, game_field)  # type: ignore


    def _update_path(self, target: Entity, game_field) -> None:
        start = tuple(self.pos)
        goal = tuple(target.pos)
        self._path = game_field.bfs_path(start, goal)
