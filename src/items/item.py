from typing import Callable, Optional

class Item:
    def __init__(self, name: str, icon, description: str, 
                 use: Optional[Callable] = None) -> None:
        self.name = name
        self.icon = icon
        self.description = description
        self.use = use