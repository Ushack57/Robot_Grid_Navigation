"""
Configuration and utilities module for the Robot Grid Navigation System.

Provides constants, helper functions, and configuration settings.
"""

# Grid Configuration
GRID_SIZE = 10
OBSTACLE_DENSITY = 0.2  # 20% of grid cells will be obstacles
MAX_SIMULATION_STEPS = 1000

# Movement Directions
DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

# Display Settings
VERBOSE_OUTPUT = True
DISPLAY_PATH_VISUALIZATION = True
DISPLAY_MOVEMENT_LOG = True


def manhattan_distance(pos1: tuple, pos2: tuple) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_adjacent(pos1: tuple, pos2: tuple) -> bool:
    """
    Check if two positions are adjacent.

    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)

    Returns:
        True if positions are adjacent, False otherwise
    """
    distance = manhattan_distance(pos1, pos2)
    return distance == 1
