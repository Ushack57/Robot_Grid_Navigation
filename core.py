"""
Robot Grid Navigation Core Module

Consolidated module containing:
- Configuration and utilities
- Grid environment management
- Robot implementation
- Perception system
- Decision-making AI (BFS + Exploration)
- Simulation orchestration
"""

import random
from typing import Tuple, Optional, List, Dict, Deque, Set
from collections import deque


# ============================================================================
# CONFIGURATION & UTILITIES
# ============================================================================

# Grid Configuration
GRID_SIZE = 10
OBSTACLE_DENSITY = 0.2
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
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def is_adjacent(pos1: tuple, pos2: tuple) -> bool:
    """Check if two positions are adjacent."""
    distance = manhattan_distance(pos1, pos2)
    return distance == 1


# ============================================================================
# GRID ENVIRONMENT
# ============================================================================

class GridEnvironment:
    """Represents a 10x10 grid-based environment for robot navigation."""

    GRID_SIZE = 10
    EMPTY = 0
    OBSTACLE = 1
    ROBOT = 2
    GOAL = 3

    def __init__(self, obstacle_density: float = 0.2, seed: int = None):
        """Initialize the grid environment."""
        if seed is not None:
            random.seed(seed)

        self.grid = [[self.EMPTY for _ in range(self.GRID_SIZE)]
                     for _ in range(self.GRID_SIZE)]
        self.obstacle_density = obstacle_density
        self.obstacles: Set[Tuple[int, int]] = set()

        self._initialize_positions()
        self._generate_obstacles()

    def _initialize_positions(self) -> None:
        """Initialize start and goal positions."""
        self.start_pos = (0, 0)
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

            if pos != self.start_pos and pos != self.goal_pos and pos not in self.obstacles:
                self.obstacles.add(pos)
                self.grid[x][y] = self.OBSTACLE
                placed += 1

            attempts += 1

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid (within bounds and not an obstacle)."""
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
        """Create a visual representation of the grid."""
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


# ============================================================================
# ROBOT
# ============================================================================

class Robot:
    """Represents an autonomous robot in the grid environment."""

    def __init__(self, start_pos: Tuple[int, int]):
        """Initialize the robot."""
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.movement_history = [start_pos]
        self.moves_count = 0

    def move(self, direction: str) -> bool:
        """Move the robot in a specified direction."""
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
        """Calculate total Manhattan distance traveled."""
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
        """Get statistics about the robot's movement."""
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


# ============================================================================
# ROBOT PERCEPTION
# ============================================================================

class RobotPerception:
    """Handles robot perception of the grid environment."""

    DIRECTIONS = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
    }

    def __init__(self, environment: GridEnvironment):
        """Initialize robot perception."""
        self.environment = environment

    def get_surrounding_cells(self, robot_pos: Tuple[int, int]) -> Dict[str, Tuple[int, int]]:
        """Get the surrounding cells in all four directions."""
        x, y = robot_pos
        surrounding = {}

        for direction, (dx, dy) in self.DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            surrounding[direction] = (new_x, new_y)

        return surrounding

    def get_valid_moves(self, robot_pos: Tuple[int, int]) -> List[str]:
        """Get all valid moves (not blocked by obstacles or boundaries)."""
        valid_moves = []
        surrounding = self.get_surrounding_cells(robot_pos)

        for direction, position in surrounding.items():
            if self.environment.is_valid_position(position[0], position[1]):
                valid_moves.append(direction)

        return valid_moves

    def detect_obstacles(self, robot_pos: Tuple[int, int]) -> Dict[str, bool]:
        """Detect if there are obstacles in each direction."""
        obstacle_map = {}
        surrounding = self.get_surrounding_cells(robot_pos)

        for direction, (x, y) in surrounding.items():
            is_blocked = not self.environment.is_valid_position(x, y)
            obstacle_map[direction] = is_blocked

        return obstacle_map

    def locate_goal(self, robot_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Locate the goal position relative to the robot."""
        return self.environment.get_goal_position()

    def calculate_manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate_direction(self, robot_pos: Tuple[int, int], direction: str) -> int:
        """Evaluate a direction by calculating distance to goal after moving."""
        dx, dy = self.DIRECTIONS[direction]
        new_pos = (robot_pos[0] + dx, robot_pos[1] + dy)
        goal_pos = self.locate_goal(robot_pos)

        return self.calculate_manhattan_distance(new_pos, goal_pos)

    def get_perception_data(self, robot_pos: Tuple[int, int]) -> Dict:
        """Get comprehensive perception data about the current position."""
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


# ============================================================================
# DECISION MAKING
# ============================================================================

class DecisionMaker:
    """AI decision-making engine using BFS with fallback exploration."""

    def __init__(self, perception: RobotPerception):
        """Initialize the decision maker."""
        self.perception = perception
        self.cached_path = None
        self.cached_start_pos = None
        self.explored_cells = set()
        self.exploration_mode = False

    def reset(self) -> None:
        """Reset decision maker state for a new simulation."""
        self.cached_path = None
        self.cached_start_pos = None
        self.explored_cells = set()
        self.exploration_mode = False

    def _bfs_find_path(self, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]) -> Optional[List[str]]:
        """Find the shortest path from start to goal using BFS."""
        if start_pos == goal_pos:
            return []

        queue: Deque[Tuple[Tuple[int, int], List[str]]
                     ] = deque([(start_pos, [])])
        visited = {start_pos}

        while queue:
            current_pos, path = queue.popleft()

            valid_moves = self.perception.get_valid_moves(current_pos)

            for direction in valid_moves:
                dx, dy = self.perception.DIRECTIONS[direction]
                next_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if next_pos == goal_pos:
                    return path + [direction]

                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [direction]))

        return None

    def get_best_move(self, robot_pos: Tuple[int, int]) -> Optional[str]:
        """Determine the best move using BFS pathfinding with exploration fallback."""
        goal_pos = self.perception.locate_goal(robot_pos)

        if not self.exploration_mode:
            if (self.cached_path is None or self.cached_start_pos != robot_pos):
                self.cached_path = self._bfs_find_path(robot_pos, goal_pos)
                self.cached_start_pos = robot_pos

            if self.cached_path is not None and len(self.cached_path) > 0:
                return self.cached_path[0]

            if self.cached_path is None:
                self.exploration_mode = True
                self.explored_cells = {robot_pos}

        if self.exploration_mode:
            return self._explore_next_move(robot_pos)

        return None

    def _explore_next_move(self, robot_pos: Tuple[int, int]) -> Optional[str]:
        """Get the next move during exploration mode."""
        valid_moves = self.perception.get_valid_moves(robot_pos)

        if not valid_moves:
            return None

        for direction in valid_moves:
            dx, dy = self.perception.DIRECTIONS[direction]
            next_pos = (robot_pos[0] + dx, robot_pos[1] + dy)

            if next_pos not in self.explored_cells:
                self.explored_cells.add(next_pos)
                return direction

        for direction in valid_moves:
            dx, dy = self.perception.DIRECTIONS[direction]
            next_pos = (robot_pos[0] + dx, robot_pos[1] + dy)

            next_valid_moves = self.perception.get_valid_moves(next_pos)
            has_unexplored = any(
                (next_pos[0] + self.perception.DIRECTIONS[d][0],
                 next_pos[1] + self.perception.DIRECTIONS[d][1]) not in self.explored_cells
                for d in next_valid_moves
            )

            if has_unexplored:
                return direction

        return None

    def get_best_moves_ranked(self, robot_pos: Tuple[int, int]) -> List[Tuple[str, int]]:
        """Get all valid moves ranked by distance to goal."""
        goal_pos = self.perception.locate_goal(robot_pos)
        valid_moves = self.perception.get_valid_moves(robot_pos)

        if not valid_moves:
            return []

        move_distances = []
        for direction in valid_moves:
            distance = self.perception.evaluate_direction(robot_pos, direction)
            move_distances.append((direction, distance))

        move_distances.sort(key=lambda x: x[1])

        return move_distances

    def is_goal_reachable(self, robot_pos: Tuple[int, int]) -> bool:
        """Check if goal is reachable from current position using BFS."""
        goal_pos = self.perception.locate_goal(robot_pos)
        path = self._bfs_find_path(robot_pos, goal_pos)
        return path is not None

    def make_decision(self, robot_pos: Tuple[int, int]) -> Tuple[bool, Optional[str]]:
        """Make a decision about the next move."""
        best_move = self.get_best_move(robot_pos)

        if best_move is None:
            return (False, None)

        return (True, best_move)

    def get_decision_info(self, robot_pos: Tuple[int, int]) -> dict:
        """Get detailed decision information."""
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


# ============================================================================
# SIMULATION
# ============================================================================

class RobotSimulation:
    """Orchestrates the robot navigation simulation."""

    def __init__(self, environment: GridEnvironment, seed: int = None):
        """Initialize the simulation."""
        self.environment = environment

        start_pos = environment.get_start_position()
        self.robot = Robot(start_pos)

        self.perception = RobotPerception(environment)
        self.decision_maker = DecisionMaker(self.perception)

        self.goal_pos = environment.get_goal_position()
        self.is_running = False
        self.is_success = False
        self.max_steps = 1000
        self.step_count = 0
        self.movement_log = []

    def reset(self) -> None:
        """Reset the simulation to initial state."""
        self.robot.reset()
        self.decision_maker.reset()
        self.is_running = False
        self.is_success = False
        self.step_count = 0
        self.movement_log = []

    def step(self) -> bool:
        """Execute a single simulation step."""
        current_pos = self.robot.get_position()

        if current_pos == self.goal_pos:
            self.is_success = True
            return False

        if self.step_count >= self.max_steps:
            return False

        can_move, direction = self.decision_maker.make_decision(current_pos)

        if not can_move:
            return False

        self.robot.move(direction)
        self.step_count += 1

        decision_info = self.decision_maker.get_decision_info(current_pos)
        self.movement_log.append({
            'step': self.step_count,
            'from_position': current_pos,
            'to_position': self.robot.get_position(),
            'direction': direction,
            'distance_to_goal': decision_info['distance_to_goal'],
            'valid_moves': decision_info['valid_moves']
        })

        return True

    def run(self, verbose: bool = True) -> Dict:
        """Run the complete simulation."""
        self.is_running = True

        if verbose:
            print("=" * 60)
            print("ROBOT GRID NAVIGATION SIMULATION")
            print("=" * 60)
            print(f"\nEnvironment: {self.environment}")
            print(f"Start Position: {self.robot.start_pos}")
            print(f"Goal Position: {self.goal_pos}")
            print(f"Obstacles: {len(self.environment.get_obstacles())}")
            print("\n" + "-" * 60)
            print("STARTING SIMULATION...")
            print("-" * 60 + "\n")

        while self.step():
            if verbose and self.step_count % 10 == 0:
                current_pos = self.robot.get_position()
                distance = self.perception.calculate_manhattan_distance(
                    current_pos, self.goal_pos
                )
                print(f"Step {self.step_count}: Robot at {current_pos}, " +
                      f"Distance to goal: {distance}")

        self.is_running = False
        return self.get_results(verbose=verbose)

    def get_results(self, verbose: bool = False) -> Dict:
        """Get simulation results."""
        final_pos = self.robot.get_position()
        final_distance = self.perception.calculate_manhattan_distance(
            final_pos, self.goal_pos
        )

        results = {
            'success': self.is_success,
            'steps_taken': self.step_count,
            'final_position': final_pos,
            'goal_position': self.goal_pos,
            'distance_to_goal': final_distance,
            'movement_history': self.robot.get_movement_history(),
            'movement_log': self.movement_log,
            'robot_stats': self.robot.get_stats(),
            'max_steps_exceeded': self.step_count >= self.max_steps
        }

        if verbose:
            print("\n" + "=" * 60)
            print("SIMULATION RESULTS")
            print("=" * 60)

            if self.is_success:
                print(f"\nSUCCESS! Robot reached the goal!")
                print(f"  Steps taken: {self.step_count}")
                print(
                    f"  Path length: {len(results['movement_history'])} positions")
            else:
                if self.step_count >= self.max_steps:
                    print(
                        f"\nFAILED: Maximum steps ({self.max_steps}) exceeded")
                else:
                    print(f"\nFAILED: Robot got stuck (no valid moves)")
                print(f"  Steps taken: {self.step_count}")
                print(f"  Final position: {final_pos}")
                print(f"  Distance to goal: {final_distance}")

            print("\n" + "-" * 60)

        return results

    def visualize_path(self) -> str:
        """Visualize the robot's path on the grid."""
        visual = "Grid visualization (S=Start, G=Goal, *=Path, #=Obstacle):\n\n"
        path = set(self.robot.get_movement_history())

        for x in range(self.environment.GRID_SIZE):
            for y in range(self.environment.GRID_SIZE):
                if (x, y) == self.environment.get_start_position():
                    visual += "S "
                elif (x, y) == self.goal_pos:
                    visual += "G "
                elif (x, y) == self.robot.get_position():
                    visual += "R "
                elif (x, y) in path:
                    visual += "* "
                elif (x, y) in self.environment.get_obstacles():
                    visual += "# "
                else:
                    visual += ". "
            visual += "\n"

        return visual

    def __repr__(self) -> str:
        """String representation of the simulation."""
        status = "running" if self.is_running else "idle"
        return f"RobotSimulation(status={status}, steps={self.step_count})"
