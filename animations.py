import time
import random

class Animations:
    """Terminal animation effects."""
    
    @staticmethod
    def fade_in(text: str, delay: float = 0.05):
        """Print text with fade-in effect (character by character)."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def flash(text: str, times: int = 3, delay: float = 0.2):
        """Flash text on and off."""
        from ui import Terminal
        for _ in range(times):
            print(f"\r{Terminal.bold(Terminal.color(text, 'YELLOW'))}", end='', flush=True)
            time.sleep(delay)
            print(f"\r{' ' * len(text)}", end='', flush=True)
            time.sleep(delay)
        print(f"\r{text}")
    
    @staticmethod
    def loading_bar(duration: float = 2.0, width: int = 30):
        """Show a loading bar."""
        from ui import Terminal
        start = time.time()
        while time.time() - start < duration:
            elapsed = time.time() - start
            progress = int((elapsed / duration) * width)
            bar = '█' * progress + '░' * (width - progress)
            percentage = int((elapsed / duration) * 100)
            print(f"\r[{bar}] {percentage}%", end='', flush=True)
            time.sleep(0.05)
        print(f"\r[{'█' * width}] 100%")
    
    @staticmethod
    def damage_text(damage: int, is_player: bool = False):
        """Display damage text animation."""
        from ui import Terminal
        color = 'RED' if is_player else 'YELLOW'
        text = Terminal.bold(Terminal.color(f"-{damage}", color))
        Animations.flash(text, times=2, delay=0.1)
    
    @staticmethod
    def level_up_animation():
        """Display level up animation."""
        from ui import Terminal
        Terminal.clear()
        print("\n" * 5)
        Animations.fade_in(Terminal.bold(Terminal.color("★ LEVEL UP! ★", 'YELLOW')), delay=0.03)
        time.sleep(0.5)
        print(Terminal.bold(Terminal.color("✨ You feel stronger! ✨", 'CYAN')))
        time.sleep(2)
