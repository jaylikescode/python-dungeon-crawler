import random
from typing import List, Tuple

class Entity:
    """Base entity class."""
    
    def __init__(self, name: str, x: int, y: int, health: int):
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
    
    def take_damage(self, damage: int) -> int:
        """Take damage."""
        self.health = max(0, self.health - damage)
        return damage
    
    def is_alive(self) -> bool:
        """Check if entity is alive."""
        return self.health > 0


class Enemy(Entity):
    """Enemy entity."""
    
    def __init__(self, name: str, x: int, y: int, health: int, damage: int, xp_reward: int):
        super().__init__(name, x, y, health)
        self.damage = damage
        self.xp_reward = xp_reward
        self.defense = 2
    
    def attack(self) -> int:
        """Calculate attack damage."""
        base_damage = self.damage
        variation = random.randint(-1, 2)
        return max(1, base_damage + variation)


class EnemyFactory:
    """Factory for creating enemies."""
    
    ENEMY_TYPES = {
        'goblin': {'health': 15, 'damage': 3, 'xp': 25},
        'orc': {'health': 30, 'damage': 6, 'xp': 50},
        'skeleton': {'health': 20, 'damage': 4, 'xp': 40},
        'troll': {'health': 50, 'damage': 8, 'xp': 75},
        'dragon': {'health': 100, 'damage': 15, 'xp': 200},
    }
    
    @staticmethod
    def create_enemy(enemy_type: str, x: int, y: int) -> Enemy:
        """Create an enemy of specified type."""
        if enemy_type not in EnemyFactory.ENEMY_TYPES:
            enemy_type = random.choice(list(EnemyFactory.ENEMY_TYPES.keys()))
        
        stats = EnemyFactory.ENEMY_TYPES[enemy_type]
        return Enemy(
            name=enemy_type.capitalize(),
            x=x,
            y=y,
            health=stats['health'],
            damage=stats['damage'],
            xp_reward=stats['xp']
        )
    
    @staticmethod
    def create_random_enemy(x: int, y: int, difficulty: int = 1) -> Enemy:
        """Create a random enemy based on difficulty level."""
        enemies = list(EnemyFactory.ENEMY_TYPES.keys())
        
        # Higher difficulty = stronger enemies
        if difficulty < 3:
            enemy_type = random.choice(enemies[:2])  # Goblin, Orc
        elif difficulty < 5:
            enemy_type = random.choice(enemies[1:4])  # Orc, Skeleton, Troll
        else:
            enemy_type = random.choice(enemies)  # Any enemy
        
        return EnemyFactory.create_enemy(enemy_type, x, y)
    
    @staticmethod
    def spawn_enemies(count: int, dungeon_width: int, dungeon_height: int, 
                      difficulty: int = 1) -> List[Enemy]:
        """Spawn multiple enemies in random positions."""
        enemies = []
        for _ in range(count):
            x = random.randint(1, dungeon_width - 2)
            y = random.randint(1, dungeon_height - 2)
            enemy = EnemyFactory.create_random_enemy(x, y, difficulty)
            enemies.append(enemy)
        return enemies
