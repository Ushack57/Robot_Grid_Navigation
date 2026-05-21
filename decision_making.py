"""
Decision-Making Algorithm Module

Implements BFS (Breadth-First Search) AI that:
- Finds and follows the shortest path to goal when reachable
- Falls back to exploration mode when goal is unreachable
- Explores available space until hitting a dead end
- Properly detects when no more moves are possible
"""

from typing import Tuple, Optional, List, Dict, Deque
from collections import deque
from perception import RobotPerception


class DecisionMaker:
    """AI decision-making engine using BFS with fallback exploration."""

    def __init__(self, perception: RobotPerception):
        """
        Initialize the decision maker.

        Args:
            perception: RobotPerception instance for sensing the environment
        """
        self.perception = perception
        self.cached_path = None
        self.cached_start_pos = None
        self.explored_cells = set()  # Track explored cells during exploration mode
        self.exploration_mode = False  # Flag for exploration mode

    def reset(self) -> None:
        """Reset decision maker state for a new simulation."""
        self.cached_path = None
        self.cached_start_pos = None
        self.explored_cells = set()
        self.exploration_mode = False

    def _bfs_find_path(self, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]) -> Optional[List[str]]:
        """
        Find the shortest path from start to goal using BFS.

        Args:
            start_pos: Robot's current position
            goal_pos: Target goal position

        Returns:
            List of directions to reach goal, or None if no path exists
        """
        if start_pos == goal_pos:
            return []

        # BFS queue: (position, path_taken)
        queue: Deque[Tuple[Tuple[int, int], List[str]]
                     ] = deque([(start_pos, [])])
        visited = {start_pos}

        while queue:
            current_pos, path = queue.popleft()

            # Get all valid moves from current position
            valid_moves = self.perception.get_valid_moves(current_pos)

            for direction in valid_moves:
                dx, dy = self.perception.DIRECTIONS[direction]
                next_pos = (current_pos[0] + dx, current_pos[1] + dy)

                # Check if we reached the goal
                if next_pos == goal_pos:
                    return path + [direction]

                # Add to queue if not visited
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [direction]))

        # No path found
        return None

    def get_best_move(self, robot_pos: Tuple[int, int]) -> Optional[str]:
        """
        Determine the best move using BFS pathfinding with exploration fallback.

        Primary: Uses BFS to find optimal path to goal
        Fallback: If no path exists, explores available space

        Args:
            robot_pos: Current position of the robot

        Returns:
            Best direction to move, or None if stuck
        """
        goal_pos = self.perception.locate_goal(robot_pos)

        # Try to find path to goal if not in exploration mode yet
        if not self.exploration_mode:
            # Check if path needs to be recalculated
            if (self.cached_path is None or self.cached_start_pos != robot_pos):
                self.cached_path = self._bfs_find_path(robot_pos, goal_pos)
                self.cached_start_pos = robot_pos

            # If path exists, follow it
            if self.cached_path is not None and len(self.cached_path) > 0:
                return self.cached_path[0]

            # No path to goal found, switch to exploration mode
            if self.cached_path is None:
                self.exploration_mode = True
                self.explored_cells = {robot_pos}  # Mark start as explored

        # Exploration mode: explore available space
        if self.exploration_mode:
            return self._explore_next_move(robot_pos)

        return None

    def _explore_next_move(self, robot_pos: Tuple[int, int]) -> Optional[str]:
        """
        Get the next move during exploration mode.

        Tries to move to unexplored adjacent cells. If all adjacent cells
        are explored, tries any valid move. If no valid moves, returns None (dead end).

        Args:
            robot_pos: Current position of the robot

        Returns:
            Direction to move, or None if completely stuck
        """
        valid_moves = self.perception.get_valid_moves(robot_pos)

        if not valid_moves:
            return None  # Completely stuck, dead end

        # First priority: move to unexplored cells
        for direction in valid_moves:
            dx, dy = self.perception.DIRECTIONS[direction]
            next_pos = (robot_pos[0] + dx, robot_pos[1] + dy)

            if next_pos not in self.explored_cells:
                self.explored_cells.add(next_pos)
                return direction

        # Second priority: move to any valid cell (backtracking)
        # This ensures continuous movement even when surrounded by explored cells
        for direction in valid_moves:
            dx, dy = self.perception.DIRECTIONS[direction]
            next_pos = (robot_pos[0] + dx, robot_pos[1] + dy)

            # Check if this cell has unexplored neighbors (frontier)
            next_valid_moves = self.perception.get_valid_moves(next_pos)
            has_unexplored = any(
                (next_pos[0] + self.perception.DIRECTIONS[d][0],
                 next_pos[1] + self.perception.DIRECTIONS[d][1]) not in self.explored_cells
                for d in next_valid_moves
            )

            if has_unexplored:
                return direction

        # If all reachable cells are explored, return None (dead end)
        return None

    def get_best_moves_ranked(self, robot_pos: Tuple[int, int]) -> List[Tuple[str, int]]:
        """
        Get all valid moves ranked by distance to goal.

        Args:
            robot_pos: Current position of the robot

        Returns:
            List of (direction, distance) tuples sorted by distance
        """
        goal_pos = self.perception.locate_goal(robot_pos)
        valid_moves = self.perception.get_valid_moves(robot_pos)

        if not valid_moves:
            return []

        # Evaluate each valid move by distance to goal
        move_distances = []
        for direction in valid_moves:
            distance = self.perception.evaluate_direction(robot_pos, direction)
            move_distances.append((direction, distance))

        # Sort by distance
        move_distances.sort(key=lambda x: x[1])

        return move_distances

    def is_goal_reachable(self, robot_pos: Tuple[int, int]) -> bool:
        """
        Check if goal is reachable from current position using BFS.

        Args:
            robot_pos: Current position of the robot

        Returns:
            True if goal is reachable, False otherwise
        """
        goal_pos = self.perception.locate_goal(robot_pos)
        path = self._bfs_find_path(robot_pos, goal_pos)
        return path is not None

    def make_decision(self, robot_pos: Tuple[int, int]) -> Tuple[bool, Optional[str]]:
        """
        Make a decision about the next move.

        Returns:
            Tuple of (can_move, direction)
            - can_move: True if there are valid moves, False if completely stuck
            - direction: The best/exploration move, or None if stuck
        """
        best_move = self.get_best_move(robot_pos)

        if best_move is None:
            return (False, None)

        return (True, best_move)

    def get_decision_info(self, robot_pos: Tuple[int, int]) -> dict:
        """
        Get detailed decision information.

        Args:
            robot_pos: Current position of the robot

        Returns:
            Dictionary with decision details
        """
        valid_moves = self.perception.get_valid_moves(robot_pos)
        best_move = self.get_best_move(robot_pos)
        ranked_moves = self.get_best_moves_ranked(robot_pos)
        goal_pos = self.perception.locate_goal(robot_pos)
        current_distance = self.perception.calculate_manhattan_distance(
            robot_pos, goal_pos)

        decision_info = {
            'current_position': robot_pos,
            'goal_position': goal_pos,
            'distance_to_goal': current_distance,
            'valid_moves': valid_moves,
            'best_move': best_move,
            'ranked_moves': ranked_moves,
            'is_stuck': best_move is None
        }

        return decision_info

    def __repr__(self) -> str:
        """String representation of the decision maker."""
        mode = "Exploration" if self.exploration_mode else "BFS Pathfinding"
        return f"DecisionMaker({mode})"
