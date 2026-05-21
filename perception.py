"""
Robot Perception Module

Provides the robot with the ability to:
- Detect surrounding cells
- Identify obstacles
- Locate the goal position
- Assess local environment
"""

from typing import Tuple, Dict, List, Set


class RobotPerception:
    """Handles robot perception of the grid environment."""

    # Movement directions: UP, DOWN, LEFT, RIGHT
    DIRECTIONS = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    def __init__(self, environment):
        """
        Initialize robot perception.

        Args:
            environment: GridEnvironment instance
        """
        self.environment = environment

    def get_surrounding_cells(self, robot_pos: Tuple[int, int]) -> Dict[str, Tuple[int, int]]:
        """
        Get the surrounding cells in all four directions.

        Args:
            robot_pos: Current position of the robot

        Returns:
            Dictionary with direction as key and adjacent position as value
        """
        x, y = robot_pos
        surrounding = {}

        for direction, (dx, dy) in self.DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            surrounding[direction] = (new_x, new_y)

        return surrounding

    def get_valid_moves(self, robot_pos: Tuple[int, int]) -> List[str]:
        """
        Get all valid moves (not blocked by obstacles or boundaries).

        Args:
            robot_pos: Current position of the robot

        Returns:
            List of valid direction names
        """
        valid_moves = []
        surrounding = self.get_surrounding_cells(robot_pos)

        for direction, position in surrounding.items():
            if self.environment.is_valid_position(position[0], position[1]):
                valid_moves.append(direction)

        return valid_moves

    def detect_obstacles(self, robot_pos: Tuple[int, int]) -> Dict[str, bool]:
        """
        Detect if there are obstacles in each direction.

        Args:
            robot_pos: Current position of the robot

        Returns:
            Dictionary with direction as key and obstacle presence (True/False) as value
        """
        obstacle_map = {}
        surrounding = self.get_surrounding_cells(robot_pos)

        for direction, (x, y) in surrounding.items():
            # Check if position is out of bounds or has an obstacle
            is_blocked = not self.environment.is_valid_position(x, y)
            obstacle_map[direction] = is_blocked

        return obstacle_map

    def locate_goal(self, robot_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Locate the goal position relative to the robot.

        Args:
            robot_pos: Current position of the robot

        Returns:
            Goal position coordinates
        """
        return self.environment.get_goal_position()

    def calculate_manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        Calculate Manhattan distance between two positions.

        Args:
            pos1: First position (x, y)
            pos2: Second position (x, y)

        Returns:
            Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate_direction(self, robot_pos: Tuple[int, int], direction: str) -> int:
        """
        Evaluate a direction by calculating distance to goal after moving.

        Args:
            robot_pos: Current position of the robot
            direction: Direction to evaluate

        Returns:
            Manhattan distance to goal after moving in this direction
        """
        dx, dy = self.DIRECTIONS[direction]
        new_pos = (robot_pos[0] + dx, robot_pos[1] + dy)
        goal_pos = self.locate_goal(robot_pos)

        return self.calculate_manhattan_distance(new_pos, goal_pos)

    def get_perception_data(self, robot_pos: Tuple[int, int]) -> Dict:
        """
        Get comprehensive perception data about the current position.

        Args:
            robot_pos: Current position of the robot

        Returns:
            Dictionary with all perception data
        """
        goal_pos = self.locate_goal(robot_pos)
        current_distance = self.calculate_manhattan_distance(
            robot_pos, goal_pos)

        perception = {
            'robot_position': robot_pos,
            'goal_position': goal_pos,
            'current_distance_to_goal': current_distance,
            'valid_moves': self.get_valid_moves(robot_pos),
            'obstacles': self.detect_obstacles(robot_pos),
            'surrounding_cells': self.get_surrounding_cells(robot_pos)
        }

        return perception

    def __repr__(self) -> str:
        """String representation of the perception module."""
        return "RobotPerception()"
