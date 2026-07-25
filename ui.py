import os
import sys
from typing import List, Tuple

class Terminal:
    """Handle terminal output and rendering."""
    
    # ANSI Color codes
    COLORS = {
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
    }
    
    SYMBOLS = {
        'PLAYER': '@',
        'ENEMY': 'E',
        'WALL': '#',
        'FLOOR': '.',
        'DOOR': '+',
        'CHEST': 'C',
        'STAIRS': '%',
        'POTION': 'P',
        'WEAPON': '/',
    }
    
    @staticmethod
    def clear():
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def color(text: str, color: str) -> str:
        """Apply color to text."""
        return f"{Terminal.COLORS.get(color, '')}{text}{Terminal.COLORS['RESET']}"
    
    @staticmethod
    def bold(text: str) -> str:
        """Make text bold."""
        return f"{Terminal.COLORS['BOLD']}{text}{Terminal.COLORS['RESET']}"
    
    @staticmethod
    def print_centered(text: str, width: int = 80):
        """Print text centered."""
        print(text.center(width))
    
    @staticmethod
    def print_separator(width: int = 80, char: str = '-'):
        """Print a separator line."""
        print(char * width)
    
    @staticmethod
    def print_box(text: str, width: int = 80):
        """Print text in a box."""
        print('┌' + '─' * (width - 2) + '┐')
        lines = text.split('\n')
        for line in lines:
            padding = width - len(line) - 4
            print(f"│ {line}{' ' * padding} │")
        print('└' + '─' * (width - 2) + '┘')


class GameUI:
    """Game user interface and rendering."""
    
    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
    
    def draw_map(self, dungeon_map: List[List[str]], player_pos: Tuple[int, int], 
                 enemies: List[Tuple[int, int, str]]):
        """Draw the dungeon map with player and entities."""
        display = [row[:] for row in dungeon_map]
        
        # Draw enemies
        for enemy_x, enemy_y, enemy_type in enemies:
            if 0 <= enemy_y < len(display) and 0 <= enemy_x < len(display[0]):
                display[enemy_y][enemy_x] = Terminal.color('E', 'RED')
        
        # Draw player
        px, py = player_pos
        if 0 <= py < len(display) and 0 <= px < len(display[0]):
            display[py][px] = Terminal.color('@', 'CYAN')
        
        # Render map
        print("\n" + Terminal.color("╔" + "═" * (self.width - 2) + "╗", 'BLUE'))
        for row in display:
            print(Terminal.color("║", 'BLUE') + ''.join(row) + Terminal.color("║", 'BLUE'))
        print(Terminal.color("╚" + "═" * (self.width - 2) + "╝", 'BLUE'))
    
    def draw_stats(self, player):
        """Draw player stats."""
        print("\n" + Terminal.bold("Stats:"))
        hp_color = 'GREEN' if player.health > player.max_health * 0.5 else 'RED'
        print(f"  HP: {Terminal.color(f'{player.health}/{player.max_health}', hp_color)}  "
              f"Mana: {Terminal.color(f'{player.mana}/{player.max_mana}', 'BLUE')}  "
              f"Level: {Terminal.color(player.level, 'YELLOW')}  "
              f"XP: {player.xp}/{player.xp_to_level}")
    
    def draw_message(self, message: str, message_type: str = 'INFO'):
        """Draw a game message."""
        color_map = {
            'INFO': 'WHITE',
            'SUCCESS': 'GREEN',
            'WARNING': 'YELLOW',
            'ERROR': 'RED',
            'COMBAT': 'MAGENTA',
        }
        color = color_map.get(message_type, 'WHITE')
        print(f"  {Terminal.color(message, color)}")
    
    def draw_inventory(self, inventory: List[dict]):
        """Draw player inventory."""
        Terminal.clear()
        print(Terminal.bold(Terminal.color("═══ INVENTORY ═══", 'CYAN')))
        if not inventory:
            print("  Empty")
        else:
            for i, item in enumerate(inventory, 1):
                item_str = f"{i}. {item['name']} - {item['type']}"
                if 'damage' in item:
                    item_str += f" (DMG: {item['damage']})"
                if 'healing' in item:
                    item_str += f" (Heal: {item['healing']})"
                print(f"  {item_str}")
        print("\nPress any key to continue...")
    
    def draw_menu(self, title: str, options: List[str]):
        """Draw a simple menu."""
        Terminal.clear()
        Terminal.print_centered(Terminal.bold(Terminal.color(title, 'CYAN')))
        Terminal.print_separator()
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        return input("\nChoose an option: ")
