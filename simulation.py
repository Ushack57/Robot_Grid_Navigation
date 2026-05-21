"""
Simulation Module

Controls the overall robot navigation simulation:
- Coordinates between robot, environment, perception, and decision-making
- Manages simulation loop
- Tracks simulation state
"""

from typing import Tuple, Optional, Dict
from grid_environment import GridEnvironment
from robot import Robot
from perception import RobotPerception
from decision_making import DecisionMaker


class RobotSimulation:
    """Orchestrates the robot navigation simulation."""

    def __init__(self, environment: GridEnvironment, seed: int = None):
        """
        Initialize the simulation.

        Args:
            environment: GridEnvironment instance
            seed: Optional random seed for reproducibility
        """
        self.environment = environment

        # Initialize robot at start position
        start_pos = environment.get_start_position()
        self.robot = Robot(start_pos)

        # Initialize perception and decision-making modules
        self.perception = RobotPerception(environment)
        self.decision_maker = DecisionMaker(self.perception)

        # Simulation state
        self.goal_pos = environment.get_goal_position()
        self.is_running = False
        self.is_success = False
        self.max_steps = 1000  # Prevent infinite loops
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
        """
        Execute a single simulation step.

        Returns:
            True if simulation should continue, False if terminated
        """
        current_pos = self.robot.get_position()

        # Check if goal is reached
        if current_pos == self.goal_pos:
            self.is_success = True
            return False  # Stop simulation

        # Check if max steps exceeded
        if self.step_count >= self.max_steps:
            return False  # Stop simulation

        # Make decision
        can_move, direction = self.decision_maker.make_decision(current_pos)

        if not can_move:
            # Robot is stuck (no valid moves)
            return False  # Stop simulation

        # Execute move
        self.robot.move(direction)
        self.step_count += 1

        # Log movement
        decision_info = self.decision_maker.get_decision_info(current_pos)
        self.movement_log.append({
            'step': self.step_count,
            'from_position': current_pos,
            'to_position': self.robot.get_position(),
            'direction': direction,
            'distance_to_goal': decision_info['distance_to_goal'],
            'valid_moves': decision_info['valid_moves']
        })

        return True  # Continue simulation

    def run(self, verbose: bool = True) -> Dict:
        """
        Run the complete simulation.

        Args:
            verbose: If True, print step-by-step information

        Returns:
            Dictionary with simulation results
        """
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

        # Main simulation loop
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
        """
        Get simulation results.

        Args:
            verbose: If True, print results

        Returns:
            Dictionary with simulation results
        """
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
                print(f"\n✓ SUCCESS! Robot reached the goal!")
                print(f"  Steps taken: {self.step_count}")
                print(
                    f"  Path length: {len(results['movement_history'])} positions")
            else:
                if self.step_count >= self.max_steps:
                    print(
                        f"\n✗ FAILED: Maximum steps ({self.max_steps}) exceeded")
                else:
                    print(f"\n✗ FAILED: Robot got stuck (no valid moves)")
                print(f"  Steps taken: {self.step_count}")
                print(f"  Final position: {final_pos}")
                print(f"  Distance to goal: {final_distance}")

            print("\n" + "-" * 60)

        return results

    def visualize_path(self) -> str:
        """
        Visualize the robot's path on the grid.

        Returns:
            String representation showing the path
        """
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
