"""
Grid Environment Module

Manages the grid-based environment including:
- Grid dimensions and layout
- Start and goal positions
- Obstacle placement
- Position validation
"""

import random
from typing import Tuple, List, Set


class GridEnvironment:
    """Represents a 10x10 grid-based environment for robot navigation."""

    GRID_SIZE = 10
    EMPTY = 0
    OBSTACLE = 1
    ROBOT = 2
    GOAL = 3

    def __init__(self, obstacle_density: float = 0.2, seed: int = None):
        """
        Initialize the grid environment.

        Args:
            obstacle_density: Proportion of cells to be obstacles (0.0 to 1.0)
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.grid = [[self.EMPTY for _ in range(self.GRID_SIZE)]
                     for _ in range(self.GRID_SIZE)]
        self.obstacle_density = obstacle_density
        self.obstacles: Set[Tuple[int, int]] = set()

        # Initialize positions
        self._initialize_positions()
        self._generate_obstacles()

    def _initialize_positions(self) -> None:
        """Initialize start and goal positions."""
        # Start position: top-left area
        self.start_pos = (0, 0)

        # Goal position: bottom-right area
        self.goal_pos = (self.GRID_SIZE - 1, self.GRID_SIZE - 1)

    def _generate_obstacles(self) -> None:
        """Generate random obstacles avoiding start and goal positions."""
        num_obstacles = int(
            self.GRID_SIZE * self.GRID_SIZE * self.obstacle_density)

        placed = 0
        attempts = 0
        max_attempts = 1000

        while placed < num_obstacles and attempts < max_attempts:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            pos = (x, y)

            # Don't place obstacles on start or goal positions
            if pos != self.start_pos and pos != self.goal_pos and pos not in self.obstacles:
                self.obstacles.add(pos)
                self.grid[x][y] = self.OBSTACLE
                placed += 1

            attempts += 1

    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if a position is valid (within bounds and not an obstacle).

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if position is valid, False otherwise
        """
        if not (0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE):
            return False

        if (x, y) in self.obstacles:
            return False

        return True

    def get_grid(self) -> List[List[int]]:
        """Get a copy of the current grid."""
        return [row[:] for row in self.grid]

    def get_obstacles(self) -> Set[Tuple[int, int]]:
        """Get the set of obstacle positions."""
        return self.obstacles.copy()

    def get_start_position(self) -> Tuple[int, int]:
        """Get the start position."""
        return self.start_pos

    def get_goal_position(self) -> Tuple[int, int]:
        """Get the goal position."""
        return self.goal_pos

    def visualize(self, robot_pos: Tuple[int, int] = None) -> str:
        """
        Create a visual representation of the grid.

        Args:
            robot_pos: Current position of the robot

        Returns:
            String representation of the grid
        """
        visual = ""
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                if (x, y) == self.start_pos:
                    visual += "S "
                elif (x, y) == self.goal_pos:
                    visual += "G "
                elif (x, y) == robot_pos:
                    visual += "R "
                elif (x, y) in self.obstacles:
                    visual += "# "
                else:
                    visual += ". "
            visual += "\n"

        return visual

    def __repr__(self) -> str:
        """String representation of the environment."""
        return f"GridEnvironment(size={self.GRID_SIZE}x{self.GRID_SIZE}, obstacles={len(self.obstacles)})"
