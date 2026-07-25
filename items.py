from typing import List, Dict
import random

class Item:
    """Base item class."""
    
    def __init__(self, name: str, item_type: str, description: str = ""):
        self.name = name
        self.item_type = item_type
        self.description = description
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'type': self.item_type,
            'description': self.description
        }


class Weapon(Item):
    """Weapon item."""
    
    def __init__(self, name: str, damage: int, crit_chance: float = 0.1):
        super().__init__(name, "Weapon")
        self.damage = damage
        self.crit_chance = crit_chance
    
    def to_dict(self) -> dict:
        d = super().to_dict()
        d['damage'] = self.damage
        d['crit_chance'] = self.crit_chance
        return d


class Potion(Item):
    """Potion item."""
    
    def __init__(self, name: str, healing: int, potion_type: str = "Health"):
        super().__init__(name, "Potion")
        self.healing = healing
        self.potion_type = potion_type
    
    def to_dict(self) -> dict:
        d = super().to_dict()
        d['healing'] = self.healing
        d['potion_type'] = self.potion_type
        return d


class Armor(Item):
    """Armor item."""
    
    def __init__(self, name: str, defense: int):
        super().__init__(name, "Armor")
        self.defense = defense
    
    def to_dict(self) -> dict:
        d = super().to_dict()
        d['defense'] = self.defense
        return d


class ItemLoot:
    """Loot generation system."""
    
    WEAPONS = [
        Weapon("Rusty Sword", 5, 0.1),
        Weapon("Iron Sword", 10, 0.15),
        Weapon("Steel Blade", 15, 0.2),
        Weapon("Enchanted Blade", 20, 0.25),
        Weapon("Dagger", 7, 0.3),
    ]
    
    POTIONS = [
        Potion("Health Potion", 20, "Health"),
        Potion("Greater Health Potion", 50, "Health"),
        Potion("Mana Potion", 15, "Mana"),
        Potion("Greater Mana Potion", 30, "Mana"),
    ]
    
    ARMOR = [
        Armor("Leather Armor", 2),
        Armor("Iron Armor", 5),
        Armor("Steel Armor", 8),
        Armor("Enchanted Plate", 12),
    ]
    
    @staticmethod
    def get_random_loot() -> Item:
        """Generate random loot."""
        loot_type = random.choice(['weapon', 'potion', 'armor'])
        
        if loot_type == 'weapon':
            return random.choice(ItemLoot.WEAPONS)
        elif loot_type == 'potion':
            return random.choice(ItemLoot.POTIONS)
        else:
            return random.choice(ItemLoot.ARMOR)
    
    @staticmethod
    def get_loot_by_level(level: int) -> Item:
        """Get loot based on player level."""
        # Higher level = better loot
        if level < 3:
            return ItemLoot.get_random_loot()
        elif level < 5:
            if random.random() < 0.7:
                return random.choice(ItemLoot.WEAPONS[1:])
            else:
                return ItemLoot.get_random_loot()
        else:
            if random.random() < 0.5:
                return random.choice(ItemLoot.WEAPONS[2:])
            else:
                return ItemLoot.get_random_loot()
