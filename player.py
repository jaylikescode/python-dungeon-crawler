from typing import List, Tuple
import random

class Player:
    """Player character class."""
    
    def __init__(self, name: str, x: int = 5, y: int = 5):
        self.name = name
        self.x = x
        self.y = y
        
        # Base stats
        self.level = 1
        self.xp = 0
        self.xp_to_level = 100
        
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        
        self.strength = 10
        self.defense = 5
        self.intelligence = 8
        
        # Inventory
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
    
    def take_damage(self, damage: int) -> int:
        """Take damage, considering defense."""
        actual_damage = max(1, damage - (self.defense // 2))
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Heal player."""
        self.health = min(self.max_health, self.health + amount)
    
    def restore_mana(self, amount: int):
        """Restore mana."""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def gain_xp(self, amount: int):
        """Gain experience points."""
        self.xp += amount
        if self.xp >= self.xp_to_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player."""
        self.level += 1
        self.xp = 0
        self.xp_to_level = int(self.xp_to_level * 1.2)
        
        # Stat increases
        self.max_health += 20
        self.health = self.max_health
        self.max_mana += 10
        self.mana = self.max_mana
        self.strength += 2
        self.defense += 1
    
    def add_item(self, item) -> bool:
        """Add item to inventory."""
        if len(self.inventory) < 10:  # Max 10 items
            self.inventory.append(item)
            return True
        return False
    
    def remove_item(self, index: int):
        """Remove item from inventory."""
        if 0 <= index < len(self.inventory):
            return self.inventory.pop(index)
        return None
    
    def use_item(self, index: int) -> bool:
        """Use an item."""
        if 0 <= index < len(self.inventory):
            item = self.inventory[index]
            if item.item_type == "Potion":
                if item.potion_type == "Health":
                    self.heal(item.healing)
                elif item.potion_type == "Mana":
                    self.restore_mana(item.healing)
                self.inventory.pop(index)
                return True
            elif item.item_type == "Weapon":
                self.equipped_weapon = item
                return True
            elif item.item_type == "Armor":
                self.equipped_armor = item
                self.defense += item.defense
                return True
        return False
    
    def get_attack_damage(self) -> int:
        """Calculate attack damage."""
        base_damage = self.strength
        if self.equipped_weapon:
            base_damage += self.equipped_weapon.damage
        
        # Random variation
        variation = random.randint(-2, 2)
        return max(1, base_damage + variation)
    
    def get_stats_dict(self) -> dict:
        """Get player stats as dictionary."""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'health': self.health,
            'max_health': self.max_health,
            'mana': self.mana,
            'max_mana': self.max_mana,
            'strength': self.strength,
            'defense': self.defense,
            'intelligence': self.intelligence,
        }
