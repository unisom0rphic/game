import pygame
from utils.constants import WIDTH, HEIGHT, STATUSBAR_HEIGHT, TILE_SIZE, LINE_OFFSET, WHITE, BLACK

class Statusbar:
    def __init__(self, screen, font, player, game_field, enemies):
        self.screen = screen
        self.font = font
        self.player = player
        self.game_field = game_field
        self.enemies = enemies
        self.statusbar = pygame.Surface((WIDTH, STATUSBAR_HEIGHT))
        self.PANEL_SECTION_OFFSET = WIDTH // 3

    def update_statusbar(self) -> None:
        self.statusbar.fill(BLACK)
        self._update_left_panel()
        self._update_middle_panel()
        self._update_right_panel()
        self.screen.blit(self.statusbar, (0, HEIGHT - STATUSBAR_HEIGHT))

    def _update_left_panel(self) -> None:
        player_info = self.player.get_info()
        for i, (feature, value) in enumerate(player_info.items()):
            text = f'{feature}: {value}'
            feature_surf = self.font.render(text, False, WHITE)
            self.statusbar.blit(feature_surf, (0, i * LINE_OFFSET))

    def _update_middle_panel(self) -> None:
        inv = self.player.get_inv()
        icons_in_line = inv.capacity // 2
        panel_width = TILE_SIZE * icons_in_line
        panel_height = TILE_SIZE * 2
        panel_surf = pygame.Surface((panel_width, panel_height))
        
        for i in range(inv.capacity):
            slot_index = i + 1
            item = inv.slots.get(slot_index)
            is_second_line = i >= icons_in_line
            x = TILE_SIZE * (i % icons_in_line)
            y = TILE_SIZE * int(is_second_line)
            
            slot_img = inv.SELECTED_SLOT_IMG if inv.selected == slot_index else inv.INV_SLOT_IMG
            panel_surf.blit(slot_img, (x, y))
            if item:
                panel_surf.blit(item.icon, (x, y))
        
        self.statusbar.blit(panel_surf, (self.PANEL_SECTION_OFFSET, 0))

    def _update_right_panel(self) -> None:
        panel_width = self.PANEL_SECTION_OFFSET
        panel_surf = pygame.Surface((panel_width, STATUSBAR_HEIGHT))
        env_info = self.player.get_env_info(self.game_field, self.enemies)
        weapon_info =  "Fists" if self.player.weapon is None else self.player.weapon.name
        
        for i, (key, value) in enumerate(env_info.items()):
            if isinstance(value, list):
                text = f'{key}: {", ".join(value)}'
            else:
                text = f'{key}: {value}'
                
            text_surf = self.font.render(text, False, WHITE)
            panel_surf.blit(text_surf, (0, i * LINE_OFFSET))

        # Displaying current weapon
        text_surf = self.font.render(f'Weapon: {weapon_info}', False, WHITE)
        panel_surf.blit(text_surf, (0, 5 * LINE_OFFSET))
        self.statusbar.blit(panel_surf, (self.PANEL_SECTION_OFFSET * 2, 0))