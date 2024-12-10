import subprocess
import sys

# Ensure all dependencies are installed
def install_dependencies():
    try:
        import pygame
    except ImportError:
        print("pygame is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

if __name__ == '__main__':
    
    install_dependencies()

    # Import Othello after ensuring dependencies
    from othello import Othello
    import pygame

    # Run the game
    game = Othello()
    game.run()
    pygame.quit()
