import random
from typing import Tuple
from animations import Animations
from ui import Terminal

class Combat:
    """Combat system."""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.round = 0
        self.messages = []
    
    def execute_round(self) -> bool:
        """Execute one combat round. Returns True if combat continues."""
        self.round += 1
        self.messages = []
        
        # Player attacks
        player_damage = self.player.get_attack_damage()
        actual_damage = self.enemy.take_damage(player_damage)
        
        crit = False
        if self.player.equipped_weapon and random.random() < self.player.equipped_weapon.crit_chance:
            crit = True
            actual_damage = int(actual_damage * 1.5)
            self.enemy.health = max(0, self.enemy.health + actual_damage - actual_damage)
        
        crit_text = " (CRITICAL!)" if crit else ""
        self.messages.append(f"You hit {self.enemy.name} for {actual_damage} damage!{crit_text}")
        
        if not self.enemy.is_alive():
            self.messages.append(f"{self.enemy.name} has been defeated!")
            return False
        
        # Enemy attacks
        enemy_damage = self.enemy.attack()
        actual_enemy_damage = self.player.take_damage(enemy_damage)
        self.messages.append(f"{self.enemy.name} hits you for {actual_enemy_damage} damage!")
        
        if not self.player.is_alive():
            self.messages.append("You have been defeated...")
            return False
        
        return True
    
    def render_round(self):
        """Render combat round information."""
        print(Terminal.bold(Terminal.color(f"\n=== Round {self.round} ===", 'MAGENTA')))
        for msg in self.messages:
            print(f"  {msg}")
        print(f"\n  You: {self.player.health}/{self.player.max_health} HP")
        print(f"  {self.enemy.name}: {self.enemy.health}/{self.enemy.max_health} HP")
    
    def start(self):
        """Start combat encounter."""
        Terminal.clear()
        print(Terminal.bold(Terminal.color(f"\n⚔ COMBAT START ⚔", 'RED')))
        print(f"\nYou encounter a {Terminal.color(self.enemy.name, 'RED')}!")
        print(f"Enemy HP: {self.enemy.health}")
        print(f"Your HP: {self.player.health}/{self.player.max_health}")
        input("\nPress Enter to begin combat...")
        
        while True:
            if not self.execute_round():
                self.render_round()
                break
            
            self.render_round()
            
            # Player options
            print("\nOptions:")
            print("  1. Continue attacking")
            print("  2. Use potion")
            print("  3. Defend")
            
            choice = input("\nChoose action (1-3): ").strip()
            
            if choice == "2":
                # Use potion
                if self.player.inventory:
                    print("\nInventory:")
                    for i, item in enumerate(self.player.inventory):
                        print(f"  {i + 1}. {item.name}")
                    item_choice = input("Use item (0 to cancel): ").strip()
                    if item_choice.isdigit() and 0 < int(item_choice) <= len(self.player.inventory):
                        if self.player.use_item(int(item_choice) - 1):
                            print("Item used!")
                        else:
                            print("Cannot use that item!")
                else:
                    print("No items in inventory!")
            
            input("\nPress Enter to continue...")
    
    def get_rewards(self):
        """Get rewards from defeating enemy."""
        xp = self.enemy.xp_reward
        self.player.gain_xp(xp)
        return xp


class CombatArena:
    """Multi-enemy combat arena."""
    
    def __init__(self, player, enemies: list):
        self.player = player
        self.enemies = [e for e in enemies if e.is_alive()]
        self.defeated = []
    
    def is_active(self) -> bool:
        """Check if combat is still active."""
        return len([e for e in self.enemies if e.is_alive()]) > 0 and self.player.is_alive()
    
    def execute_turn(self):
        """Execute one combat turn."""
        # Player attacks closest enemy
        closest = min(self.enemies, key=lambda e: abs(e.x - self.player.x) + abs(e.y - self.player.y))
        
        if closest.is_alive():
            damage = self.player.get_attack_damage()
            actual_damage = closest.take_damage(damage)
            print(f"You attack {closest.name} for {actual_damage} damage!")
            
            if not closest.is_alive():
                self.defeated.append(closest)
                self.player.gain_xp(closest.xp_reward)
                print(f"{closest.name} defeated! +{closest.xp_reward} XP")
        
        # Enemies attack
        for enemy in self.enemies:
            if enemy.is_alive() and (abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)) < 10:
                damage = enemy.attack()
                actual_damage = self.player.take_damage(damage)
                print(f"{enemy.name} attacks for {actual_damage} damage!")
