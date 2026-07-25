import random
from typing import List, Tuple

class Dungeon:
    """Dungeon generator and manager."""
    
    def __init__(self, width: int = 40, height: int = 20, level: int = 1):
        self.width = width
        self.height = height
        self.level = level
        self.map = []
        self.generate()
    
    def generate(self):
        """Generate dungeon map using simple algorithm."""
        # Initialize with walls
        self.map = [['#' for _ in range(self.width)] for _ in range(self.height)]
        
        # Create rooms using binary space partitioning
        self._create_rooms(1, 1, self.width - 2, self.height - 2)
    
    def _create_rooms(self, x: int, y: int, width: int, height: int, depth: int = 0):
        """Recursively create rooms."""
        if width < 10 or height < 10:
            # Create floor
            for i in range(y, y + height):
                for j in range(x, x + width):
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self.map[i][j] = '.'
            return
        
        # Randomly split vertically or horizontally
        if random.random() < 0.5:
            # Split vertically
            split_x = x + width // 2
            self._create_rooms(x, y, split_x - x - 1, height, depth + 1)
            self._create_rooms(split_x + 1, y, width - (split_x - x) - 1, height, depth + 1)
            
            # Create horizontal corridor
            for i in range(y, y + height):
                if 0 <= i < self.height and 0 <= split_x < self.width:
                    self.map[i][split_x] = '.'
        else:
            # Split horizontally
            split_y = y + height // 2
            self._create_rooms(x, y, width, split_y - y - 1, depth + 1)
            self._create_rooms(x, split_y + 1, width, height - (split_y - y) - 1, depth + 1)
            
            # Create vertical corridor
            for j in range(x, x + width):
                if 0 <= split_y < self.height and 0 <= j < self.width:
                    self.map[split_y][j] = '.'
    
    def get_valid_spawn_position(self) -> Tuple[int, int]:
        """Get a valid position to spawn player."""
        while True:
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            if self.map[y][x] == '.':
                return (x, y)
    
    def get_valid_positions(self, count: int) -> List[Tuple[int, int]]:
        """Get multiple valid positions."""
        positions = []
        attempts = 0
        max_attempts = 100
        
        while len(positions) < count and attempts < max_attempts:
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            if self.map[y][x] == '.' and (x, y) not in positions:
                positions.append((x, y))
            attempts += 1
        
        return positions
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if position is walkable."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map[y][x] == '.'
        return False
    
    def get_display_map(self) -> List[List[str]]:
        """Get map for display."""
        # Convert to strings with colors
        from ui import Terminal
        display_map = []
        for row in self.map:
            display_row = []
            for cell in row:
                if cell == '#':
                    display_row.append(Terminal.color('#', 'BLUE'))
                else:
                    display_row.append('.')
            display_map.append(display_row)
        return display_map
