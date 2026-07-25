import random
import sys
from typing import Optional
from player import Player
from dungeon import Dungeon
from entities import EnemyFactory, Enemy
from items import ItemLoot
from combat import Combat
from ui import Terminal, GameUI
from animations import Animations


class Game:
    """Main game class."""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.dungeon: Optional[Dungeon] = None
        self.ui: Optional[GameUI] = None
        self.enemies = []
        self.current_level = 1
        self.running = False
    
    def start(self):
        """Start the game."""
        Terminal.clear()
        Animations.fade_in(Terminal.bold(Terminal.color("═══ DUNGEON CRAWLER ═══", 'CYAN')), delay=0.02)
        print("\nWelcome to the Dungeon Crawler!")
        print("\nNavigate through dungeons, defeat enemies, and collect loot.")
        print("Survive as long as you can and reach the deepest levels!\n")
        
        name = input("Enter your character name: ").strip()
        if not name:
            name = "Adventurer"
        
        self.player = Player(name)
        self.ui = GameUI()
        self.running = True
        
        self.main_loop()
    
    def new_dungeon(self):
        """Generate a new dungeon level."""
        self.dungeon = Dungeon(width=40, height=20, level=self.current_level)
        
        # Spawn player
        start_x, start_y = self.dungeon.get_valid_spawn_position()
        self.player.x = start_x
        self.player.y = start_y
        
        # Spawn enemies
        enemy_count = 3 + self.current_level
        enemy_positions = self.dungeon.get_valid_positions(enemy_count)
        self.enemies = []
        
        for x, y in enemy_positions:
            enemy = EnemyFactory.create_random_enemy(x, y, difficulty=self.current_level)
            self.enemies.append(enemy)
    
    def handle_input(self) -> str:
        """Handle player input."""
        print("\nControls:")
        print("  Movement: WASD or arrow keys")
        print("  I: Inventory")
        print("  H: Help")
        print("  Q: Quit")
        
        return input("\nAction: ").strip().upper()
    
    def move_player(self, direction: str) -> bool:
        """Move player in direction."""
        dx, dy = 0, 0
        
        if direction == 'W':
            dy = -1
        elif direction == 'S':
            dy = 1
        elif direction == 'A':
            dx = -1
        elif direction == 'D':
            dx = 1
        else:
            return False
        
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        if self.dungeon.is_walkable(new_x, new_y):
            self.player.x = new_x
            self.player.y = new_y
            
            # Check for enemy collision
            for enemy in self.enemies:
                if enemy.x == new_x and enemy.y == new_y and enemy.is_alive():
                    self.start_combat(enemy)
                    return True
            
            # Check for loot
            if random.random() < 0.1:  # 10% chance to find loot
                loot = ItemLoot.get_loot_by_level(self.player.level)
                if self.player.add_item(loot):
                    self.ui.draw_message(f"Found {loot.name}!", 'SUCCESS')
                else:
                    self.ui.draw_message("Inventory full!", 'WARNING')
            
            return True
        else:
            self.ui.draw_message("Can't move there!", 'ERROR')
            return False
    
    def start_combat(self, enemy: Enemy):
        """Start combat with an enemy."""
        combat = Combat(self.player, enemy)
        combat.start()
        
        if self.player.is_alive():
            xp_gained = combat.get_rewards()
            Terminal.clear()
            self.ui.draw_message(f"Victory! Gained {xp_gained} XP", 'SUCCESS')
            
            if self.player.level > self.current_level:
                Animations.level_up_animation()
            
            # Remove defeated enemy
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        else:
            self.game_over()
    
    def show_inventory(self):
        """Show player inventory."""
        Terminal.clear()
        print(Terminal.bold(Terminal.color("═══ INVENTORY ═══", 'CYAN')))
        
        if not self.player.inventory:
            print("  Empty")
        else:
            for i, item in enumerate(self.player.inventory, 1):
                item_str = f"{i}. {item.name} - {item.item_type}"
                if hasattr(item, 'damage'):
                    item_str += f" (DMG: {item.damage})"
                if hasattr(item, 'healing'):
                    item_str += f" (Heal: {item.healing})"
                print(f"  {item_str}")
        
        print("\nOptions:")
        print("  U <number>: Use/Equip item")
        print("  D <number>: Drop item")
        print("  B: Back to game")
        
        choice = input("\n> ").strip().upper()
        
        if choice.startswith('U'):
            try:
                idx = int(choice.split()[1]) - 1
                if self.player.use_item(idx):
                    self.ui.draw_message(f"Used {self.player.inventory[idx].name}!", 'SUCCESS')
            except:
                pass
        elif choice.startswith('D'):
            try:
                idx = int(choice.split()[1]) - 1
                item = self.player.remove_item(idx)
                if item:
                    self.ui.draw_message(f"Dropped {item.name}!", 'INFO')
            except:
                pass
    
    def show_help(self):
        """Show help screen."""
        Terminal.clear()
        print(Terminal.bold(Terminal.color("═══ HELP ═══", 'CYAN')))
        print("""
  OBJECTIVE: Explore the dungeon and survive!
  
  CONTROLS:
    WASD - Move around
    I    - Open inventory
    H    - Help (this screen)
    Q    - Quit game
  
  GAMEPLAY:
    - Defeat enemies to gain experience and level up
    - Collect loot from defeated enemies
    - Find potions to restore health and mana
    - Equip weapons and armor to become stronger
    - Reach deeper levels to face tougher challenges
  
  STATS:
    - HP: Health points, lose all to die
    - Mana: Resource for special abilities
    - Strength: Affects damage dealt
    - Defense: Reduces incoming damage
  
  TIPS:
    - Avoid fights when your HP is low
    - Stock up on potions before exploring
    - Stronger enemies give more XP and better loot
        """)
        input("\nPress Enter to continue...")
    
    def main_loop(self):
        """Main game loop."""
        self.new_dungeon()
        
        while self.running and self.player.is_alive():
            Terminal.clear()
            
            # Render dungeon
            display_map = self.dungeon.get_display_map()
            self.ui.draw_map(display_map, (self.player.x, self.player.y),
                           [(e.x, e.y, e.name) for e in self.enemies if e.is_alive()])
            
            # Render stats
            self.ui.draw_stats(self.player)
            
            # Get player input
            action = self.handle_input()
            
            if action in ['W', 'A', 'S', 'D']:
                self.move_player(action)
            elif action == 'I':
                self.show_inventory()
            elif action == 'H':
                self.show_help()
            elif action == 'Q':
                self.quit_game()
            
            # Remove all defeated enemies
            self.enemies = [e for e in self.enemies if e.is_alive()]
            
            # Check if level cleared
            if not any(e.is_alive() for e in self.enemies):
                print("\n" + Terminal.bold(Terminal.color("✓ Level cleared!", 'GREEN')))
                self.current_level += 1
                input("Press Enter to proceed to next level...")
                self.new_dungeon()
    
    def game_over(self):
        """Handle game over."""
        Terminal.clear()
        print(Terminal.bold(Terminal.color("\n☠ GAME OVER ☠", 'RED')))
        print(f"\nCharacter: {self.player.name}")
        print(f"Level Reached: {self.current_level}")
        print(f"Final Level: {self.player.level}")
        print(f"Total XP: {self.player.xp}")
        
        self.running = False
    
    def quit_game(self):
        """Quit the game."""
        print("\nThanks for playing!")
        self.running = False
        sys.exit(0)


def main():
    """Entry point."""
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
