import pygame
from collections import deque
from utils.constants import WIDTH, HEIGHT, STATUSBAR_HEIGHT, TILE_SIZE

class Tile:
    def __init__(self, image, pos, entity=None, items=None, have_collision=False):
        self.image = image
        self.pos = pos
        self.entity = entity
        self.items = items if items is not None else []
        self.have_collision = have_collision

class GameField:
    def __init__(self, background_image) -> None:
        self.width = WIDTH // TILE_SIZE
        self.height = (HEIGHT - STATUSBAR_HEIGHT) // TILE_SIZE
        self._tiles = [
            [Tile(background_image, (r, c)) 
            for c in range(self.width)]
            for r in range(self.height)
        ]
        self.field_surf = pygame.Surface((WIDTH, HEIGHT))

    def get_tile(self, pos):
        r, c = pos
        return self._tiles[r][c]

    def redraw(self) -> None:
        self.field_surf.fill((0, 0, 0))
        for r in range(self.height):
            for c in range(self.width):
                tile = self._tiles[r][c]
                x, y = c * TILE_SIZE, r * TILE_SIZE
                
                if tile.entity:
                    self.field_surf.blit(tile.entity.surf, (x, y))
                else:
                    self.field_surf.blit(tile.image, (x, y))
                    if tile.items:
                        self.field_surf.blit(tile.items[0].icon, (x, y))

    def add_wall(self, wall_img, row: int, col: int, direction, length: int) -> None:
        dr, dc = direction.value
        for i in range(length):
            r = row + dr * i
            c = col + dc * i
            if 0 <= r < self.height and 0 <= c < self.width:
                self._tiles[r][c] = Tile(wall_img, (r, c), have_collision=True)

    def bfs_path(self, start, goal):
        if start == goal:
            return []
            
        queue = deque([start])
        visited = {start: None}
        
        while queue:
            r, c = queue.popleft()
            
            if (r, c) == goal:
                break
                
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = r + dr, c + dc
                
                if not (0 <= nr < self.height and 0 <= nc < self.width):
                    continue
                    
                tile = self._tiles[nr][nc]
                if (nr, nc) in visited or (tile.have_collision and not tile.entity):
                    continue
                    
                visited[(nr, nc)] = (r, c) # type: ignore
                queue.append((nr, nc))
                
        if goal not in visited:
            return None
            
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = visited[current]
        path.reverse()
        return path

    def display_field(self):
        return self.field_surf