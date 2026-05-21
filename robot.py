"""
Robot Module

Represents the robot agent that:
- Moves within the grid
- Tracks its position and state
- Records movement history
"""

from typing import Tuple, Optional, List


class Robot:
    """Represents an autonomous robot in the grid environment."""

    def __init__(self, start_pos: Tuple[int, int]):
        """
        Initialize the robot.

        Args:
            start_pos: Starting position (x, y)
        """
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.movement_history = [start_pos]
        self.moves_count = 0

    def move(self, direction: str) -> bool:
        """
        Move the robot in a specified direction.

        Args:
            direction: Direction to move ('UP', 'DOWN', 'LEFT', 'RIGHT')

        Returns:
            True if move was executed, False otherwise
        """
        direction_map = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        if direction not in direction_map:
            return False

        dx, dy = direction_map[direction]
        new_x = self.current_pos[0] + dx
        new_y = self.current_pos[1] + dy

        # Actually move the robot
        self.current_pos = (new_x, new_y)
        self.movement_history.append(self.current_pos)
        self.moves_count += 1

        return True

    def get_position(self) -> Tuple[int, int]:
        """Get the current position of the robot."""
        return self.current_pos

    def get_movement_history(self) -> List[Tuple[int, int]]:
        """Get the complete movement history."""
        return self.movement_history.copy()

    def get_moves_count(self) -> int:
        """Get the total number of moves made."""
        return self.moves_count

    def get_distance_traveled(self) -> int:
        """
        Calculate total Manhattan distance traveled.

        Returns:
            Sum of all Manhattan distances between consecutive positions
        """
        total_distance = 0
        for i in range(1, len(self.movement_history)):
            prev_pos = self.movement_history[i-1]
            curr_pos = self.movement_history[i]
            distance = abs(prev_pos[0] - curr_pos[0]) + \
                abs(prev_pos[1] - curr_pos[1])
            total_distance += distance

        return total_distance

    def reset(self) -> None:
        """Reset the robot to its starting position."""
        self.current_pos = self.start_pos
        self.movement_history = [self.start_pos]
        self.moves_count = 0

    def get_stats(self) -> dict:
        """
        Get statistics about the robot's movement.

        Returns:
            Dictionary with movement statistics
        """
        return {
            'start_position': self.start_pos,
            'current_position': self.current_pos,
            'moves_count': self.moves_count,
            'distance_traveled': self.get_distance_traveled(),
            'movement_history': self.get_movement_history()
        }

    def __repr__(self) -> str:
        """String representation of the robot."""
        return f"Robot(pos={self.current_pos}, moves={self.moves_count})"
