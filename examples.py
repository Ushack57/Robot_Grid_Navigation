"""
Example usage demonstrations for the Robot Grid Navigation System

Shows different ways to use and customize the system
"""

from grid_environment import GridEnvironment
from robot import Robot
from perception import RobotPerception
from decision_making import DecisionMaker
from simulation import RobotSimulation


def example_1_basic_simulation():
    """Example 1: Run a basic simulation with default settings."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Simulation")
    print("=" * 60 + "\n")

    # Create environment
    env = GridEnvironment(obstacle_density=0.15, seed=123)

    # Create and run simulation
    simulation = RobotSimulation(env)
    results = simulation.run(verbose=True)

    # Display results
    print(simulation.visualize_path())


def example_2_inspect_robot_perception():
    """Example 2: Inspect what the robot perceives at different positions."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Robot Perception Analysis")
    print("=" * 60 + "\n")

    env = GridEnvironment(obstacle_density=0.1, seed=42)
    perception = RobotPerception(env)

    # Analyze perception at different positions
    positions = [(1, 1), (3, 3), (5, 5), (8, 8)]

    for pos in positions:
        if env.is_valid_position(pos[0], pos[1]):
            print(f"\nPosition: {pos}")
            print("-" * 40)

            # Get perception data
            perception_data = perception.get_perception_data(pos)

            print(f"Goal: {perception_data['goal_position']}")
            print(
                f"Distance to goal: {perception_data['current_distance_to_goal']}")
            print(f"Valid moves: {perception_data['valid_moves']}")

            # Show obstacles
            obstacles = perception_data['obstacles']
            blocked_directions = [
                d for d, blocked in obstacles.items() if blocked]
            if blocked_directions:
                print(f"Blocked directions: {blocked_directions}")
            else:
                print("No blocked directions")


def example_3_trace_decision_making():
    """Example 3: Trace the decision-making process step by step."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Decision-Making Trace")
    print("=" * 60 + "\n")

    env = GridEnvironment(obstacle_density=0.1, seed=123)
    perception = RobotPerception(env)
    decision_maker = DecisionMaker(perception)

    # Start from position (1, 1)
    current_pos = (1, 1)

    print(f"Starting position: {current_pos}\n")

    # Trace decision for several steps
    for step in range(5):
        print(f"Step {step + 1}:")
        print("-" * 40)

        # Get decision info
        decision_info = decision_maker.get_decision_info(current_pos)

        print(f"Current position: {decision_info['current_position']}")
        print(f"Distance to goal: {decision_info['distance_to_goal']}")
        print(f"Valid moves: {decision_info['valid_moves']}")

        # Show ranked moves
        if decision_info['ranked_moves']:
            print(f"Best move: {decision_info['best_move']} " +
                  f"(reduces distance to {decision_info['ranked_moves'][0][1]})")
            print(f"All ranked moves:")
            for direction, distance in decision_info['ranked_moves']:
                print(f"  {direction:6s} → distance {distance}")
        else:
            print("No valid moves available!")
            break

        # Move to best position for next iteration
        best_move = decision_info['best_move']
        if best_move:
            direction_map = {
                'UP': (-1, 0), 'DOWN': (1, 0),
                'LEFT': (0, -1), 'RIGHT': (0, 1)
            }
            dx, dy = direction_map[best_move]
            current_pos = (current_pos[0] + dx, current_pos[1] + dy)
            print()


def example_4_compare_different_seeds():
    """Example 4: Compare simulation results with different random seeds."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Comparing Different Seeds")
    print("=" * 60 + "\n")

    seeds = [10, 20, 30, 40, 50]
    results_list = []

    for seed in seeds:
        env = GridEnvironment(obstacle_density=0.15, seed=seed)
        simulation = RobotSimulation(env)
        results = simulation.run(verbose=False)
        results_list.append(results)

        status = "✓" if results['success'] else "✗"
        print(f"Seed {seed}: {status} " +
              f"Steps={results['steps_taken']:4d}, " +
              f"Success={results['success']}, " +
              f"Final distance={results['distance_to_goal']}")

    # Summary
    successful = sum(1 for r in results_list if r['success'])
    print(
        f"\nSuccess rate: {successful}/{len(seeds)} ({100*successful/len(seeds):.0f}%)")

    if successful > 0:
        avg_steps = sum(r['steps_taken']
                        for r in results_list if r['success']) / successful
        print(f"Average steps (successful): {avg_steps:.1f}")


def example_5_custom_obstacle_density():
    """Example 5: Test with different obstacle densities."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Effect of Obstacle Density")
    print("=" * 60 + "\n")

    densities = [0.05, 0.10, 0.15, 0.20, 0.25]

    print(f"{'Density':<10} {'Success':<10} {'Steps':<10} {'Final Dist':<12}")
    print("-" * 45)

    for density in densities:
        env = GridEnvironment(obstacle_density=density, seed=42)
        simulation = RobotSimulation(env)
        results = simulation.run(verbose=False)

        status = "Yes" if results['success'] else "No"
        print(f"{density:<10.0%} {status:<10} {results['steps_taken']:<10} " +
              f"{results['distance_to_goal']:<12}")


def example_6_visualize_multiple_paths():
    """Example 6: Run multiple simulations and show all paths."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Multiple Paths Visualization")
    print("=" * 60 + "\n")

    num_runs = 3

    for run in range(num_runs):
        print(f"\nRun {run + 1}:")
        print("-" * 40)

        env = GridEnvironment(obstacle_density=0.15, seed=100 + run)
        simulation = RobotSimulation(env)
        results = simulation.run(verbose=False)

        status = "SUCCESS" if results['success'] else "FAILED"
        print(f"Status: {status}")
        print(f"Steps: {results['steps_taken']}")

        # Show path
        print("\nPath visualization:\n")
        print(simulation.visualize_path())


def example_7_robot_statistics():
    """Example 7: Analyze robot statistics after simulation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Robot Statistics Analysis")
    print("=" * 60 + "\n")

    env = GridEnvironment(obstacle_density=0.15, seed=789)
    simulation = RobotSimulation(env)
    results = simulation.run(verbose=False)

    stats = results['robot_stats']

    print("Robot Statistics:")
    print("-" * 40)
    print(f"Start position: {stats['start_position']}")
    print(f"End position: {stats['current_position']}")
    print(f"Total moves: {stats['moves_count']}")
    print(f"Distance traveled: {stats['distance_traveled']}")

    if stats['moves_count'] > 0:
        efficiency = stats['distance_traveled'] / stats['moves_count']
        print(f"Efficiency (distance/move): {efficiency:.2f}")

    # Show path
    print(f"\nMovement history ({len(stats['movement_history'])} positions):")
    path = " → ".join(str(pos) for pos in stats['movement_history'][:10])
    print(f"{path}...")


def run_all_examples():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " ROBOT GRID NAVIGATION - USAGE EXAMPLES ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")

    # Run examples
    example_1_basic_simulation()
    example_2_inspect_robot_perception()
    example_3_trace_decision_making()
    example_4_compare_different_seeds()
    example_5_custom_obstacle_density()
    example_6_visualize_multiple_paths()
    example_7_robot_statistics()

    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Run all examples
    run_all_examples()

    # Or run individual examples:
    # example_1_basic_simulation()
    # example_2_inspect_robot_perception()
    # example_3_trace_decision_making()
    # etc.
