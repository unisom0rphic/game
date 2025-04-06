import pygame
import game

surf = pygame.Surface((32,32))
surf.fill('black')
def test_inv():
    inv = game.Inventory(2)
    itm1 = game.Item('1', surf, '1')
    itm2 = game.Item('2', surf, '2')
    itm3 = game.Item('3', surf, '3')

    assert inv.add_item(itm1) == 1
    assert inv.add_item(itm2) == 1
    assert inv.add_item(itm3) == 0

    print(inv.slots)

if __name__ == '__main__':
    test_inv()
    
