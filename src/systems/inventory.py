class Inventory:
    def __init__(self, capacity: int, empty_slot_img, selected_slot_img):
        self.capacity = capacity
        self.slots = {}
        self.INV_SLOT_IMG = empty_slot_img
        self.SELECTED_SLOT_IMG = selected_slot_img
        self.selected = 1

    def add_item(self, item) -> bool:
        if len(self.slots) >= self.capacity:
            return False
            
        for slot in range(1, self.capacity + 1):
            if slot not in self.slots:
                self.slots[slot] = item
                return True
        return False

    def remove_item(self, slot_i: int) -> bool:
        if slot_i in self.slots:
            del self.slots[slot_i]
            return True
        return False