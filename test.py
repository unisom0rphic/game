import pygame

WIDTH, HEIGHT = 800, 640 
TILE_SIZE = 32 
FPS = 60
    
# Colors
WHITE = pygame.color.Color(255,255,255)
BLACK = pygame.color.Color(0,0,0)
GRAY = pygame.color.Color(100, 100, 100)

# Classes
class Player:
    health = 100
    armor = 0
    pos_x = 1
    pos_y = 1
    player_color = GRAY 
    player_rect = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    def __init__(self):
        self.health = 100
        print("PLAYER IS CREATED")

# Functions
def render_tile(screen: pygame.Surface, r: pygame.rect.Rect, color: pygame.color.Color, x: int, y: int) -> None:
    pygame.draw.rect(screen, BLACK, r)
    r.center = (TILE_SIZE*x-TILE_SIZE//2, TILE_SIZE*y-TILE_SIZE//2)
    pygame.draw.rect(screen, color, r)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game is gaming frfr")
    print(pygame.display.Info())

    clock = pygame.time.Clock()
    
    wall1 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)
    wall2 = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE)

    player = Player()

    # game loop
    running = True
    while running:
        screen.fill((0, 0, 0)) 

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RIGHT:
                    player.pos_x += 1
                elif event.key == pygame.K_LEFT:
                    player.pos_x -= 1
                elif event.key == pygame.K_UP:
                    player.pos_y -= 1
                elif event.key == pygame.K_DOWN:
                    player.pos_y += 1


            pygame.draw.rect(screen, GRAY, player.player_rect)
            render_tile(screen, player.player_rect, player.player_color, player.pos_x, player.pos_y)
            render_tile(screen, wall1, GRAY, 5, 6)
            render_tile(screen, wall2, GRAY, 5, 7)

            pygame.display.update()
            clock.tick(FPS)
