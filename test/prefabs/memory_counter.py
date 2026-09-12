from ursina import Ursina
from ursina.prefabs.memory_counter import MemoryCounter

if __name__ == "__main__":
    """
       Displays the amount of memory used in the bottom right corner
    """
    app = Ursina()
    MemoryCounter()
    app.run()
