"""
Visualization and Analysis Tools for Robot Grid Navigation

Provides utilities for:
- Creating detailed visualizations
- Analyzing performance metrics
- Comparing different algorithms/configurations
"""

from grid_environment import GridEnvironment
from simulation import RobotSimulation
from perception import RobotPerception
from decision_making import DecisionMaker


def analyze_single_run(seed: int = 42, obstacle_density: float = 0.15):
    """
    Perform detailed analysis of a single simulation run.

    Args:
        seed: Random seed for reproducibility
        obstacle_density: Proportion of obstacles
    """
    print("=" * 70)
    print("DETAILED ANALYSIS OF SINGLE SIMULATION RUN")
    print("=" * 70)
    print(f"Configuration: seed={seed}, obstacle_density={obstacle_density}")
    print()

    # Create and run simulation
    env = GridEnvironment(obstacle_density=obstacle_density, seed=seed)
    simulation = RobotSimulation(env)
    results = simulation.run(verbose=False)

    # Header
    print("┌─" + "─" * 68 + "─┐")
    print("│ " + "SIMULATION RESULTS".center(66) + " │")
    print("└─" + "─" * 68 + "─┘")
    print()

    # Basic results
    status = "✓ SUCCESS" if results['success'] else "✗ FAILED"
    print(f"  Status: {status}")
    print(f"  Start Position: {results['robot_stats']['start_position']}")
    print(f"  End Position: {results['final_position']}")
    print(f"  Goal Position: {results['goal_position']}")
    print()

    # Movement statistics
    print("┌─ MOVEMENT STATISTICS " + "─" * 45 + "─┐")
    print(f"│  Steps Taken: {results['steps_taken']:6d}")
    print(f"│  Path Length: {len(results['movement_history']):6d} positions")
    print(
        f"│  Distance Traveled: {results['robot_stats']['distance_traveled']:6d}")

    if results['steps_taken'] > 0:
        efficiency = results['robot_stats']['distance_traveled'] / \
            results['steps_taken']
        print(f"│  Path Efficiency: {efficiency:6.2f} (distance per step)")

    print(f"│  Distance to Goal: {results['distance_to_goal']:6d}")
    print("└" + "─" * 69 + "┘")
    print()

    # Obstacle statistics
    print("┌─ ENVIRONMENT STATISTICS " + "─" * 42 + "─┐")
    total_cells = env.GRID_SIZE * env.GRID_SIZE
    obstacle_count = len(env.get_obstacles())
    actual_density = obstacle_count / total_cells
    print(
        f"│  Grid Size: {env.GRID_SIZE}×{env.GRID_SIZE} = {total_cells} cells")
    print(f"│  Obstacle Count: {obstacle_count} cells")
    print(f"│  Obstacle Density: {actual_density:.1%}")
    print(f"│  Free Cells: {total_cells - obstacle_count} cells")
    print("└" + "─" * 69 + "┘")
    print()

    # Path visualization
    print("┌─ PATH VISUALIZATION " + "─" * 46 + "─┐")
    print(simulation.visualize_path())
    print("└" + "─" * 69 + "┘")
    print()

    # Movement log (first 10 steps)
    if results['movement_log']:
        print("┌─ MOVEMENT LOG (First 10 Steps) " + "─" * 34 + "─┐")
        for entry in results['movement_log'][:10]:
            print(f"│  Step {entry['step']:2d}: {str(entry['from_position']):8s} → " +
                  f"{str(entry['to_position']):8s} ({entry['direction']:6s})")
        if len(results['movement_log']) > 10:
            print(f"│  ... ({len(results['movement_log']) - 10} more steps)")
        print("└" + "─" * 69 + "┘")
    print()


def compare_obstacle_densities(seeds: int = 5):
    """
    Compare success rates across different obstacle densities.

    Args:
        seeds: Number of different seeds to test per density
    """
    print("=" * 70)
    print("IMPACT OF OBSTACLE DENSITY ON SUCCESS RATE")
    print("=" * 70)
    print()

    densities = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

    print(f"{'Density':<12} {'Runs':<8} {'Success':<12} {'Rate':<10} " +
          f"{'Avg Steps':<12} {'Avg Dist':<12}")
    print("─" * 70)

    for density in densities:
        successes = 0
        total_steps = 0
        total_distance = 0

        for seed in range(seeds):
            env = GridEnvironment(obstacle_density=density, seed=seed)
            simulation = RobotSimulation(env)
            results = simulation.run(verbose=False)

            if results['success']:
                successes += 1
                total_steps += results['steps_taken']

            total_distance += results['distance_to_goal']

        success_rate = successes / seeds if seeds > 0 else 0
        avg_steps = total_steps / max(successes, 1) if successes > 0 else 0
        avg_distance = total_distance / seeds

        print(f"{density:<12.0%} {seeds:<8d} {successes:<12d} " +
              f"{success_rate:<10.0%} {avg_steps:<12.1f} {avg_distance:<12.1f}")

    print()


def compare_seeds(num_seeds: int = 10, density: float = 0.15):
    """
    Compare results across different random seeds.

    Args:
        num_seeds: Number of different seeds to test
        density: Obstacle density for all tests
    """
    print("=" * 70)
    print(f"COMPARISON ACROSS {num_seeds} RANDOM SEEDS")
    print("=" * 70)
    print(f"Obstacle Density: {density:.0%}")
    print()

    results_list = []

    for seed in range(num_seeds):
        env = GridEnvironment(obstacle_density=density, seed=seed)
        simulation = RobotSimulation(env)
        results = simulation.run(verbose=False)
        results_list.append(results)

    # Print individual results
    print(f"{'Seed':<6} {'Status':<10} {'Steps':<8} {'Distance':<10} {'Path Length':<12}")
    print("─" * 70)

    for seed, results in enumerate(results_list):
        status = "✓ SUCCESS" if results['success'] else "✗ FAILED"
        path_length = len(results['movement_history'])
        print(f"{seed:<6} {status:<10} {results['steps_taken']:<8} " +
              f"{results['distance_to_goal']:<10} {path_length:<12}")

    print()

    # Summary statistics
    successful = sum(1 for r in results_list if r['success'])
    print("┌─ SUMMARY STATISTICS " + "─" * 47 + "─┐")
    print(f"│  Total Runs: {num_seeds}")
    print(
        f"│  Successful: {successful}/{num_seeds} ({100*successful/num_seeds:.1f}%)")
    print(
        f"│  Failed: {num_seeds - successful}/{num_seeds} ({100*(num_seeds-successful)/num_seeds:.1f}%)")

    if successful > 0:
        avg_steps = sum(r['steps_taken']
                        for r in results_list if r['success']) / successful
        max_steps = max((r['steps_taken']
                        for r in results_list if r['success']), default=0)
        min_steps = min((r['steps_taken']
                        for r in results_list if r['success']), default=0)
        print(f"│  ")
        print(f"│  Steps (successful runs):")
        print(f"│    Average: {avg_steps:.1f}")
        print(f"│    Min: {min_steps}")
        print(f"│    Max: {max_steps}")

    print("└" + "─" * 69 + "┘")
    print()


def perception_heatmap(seed: int = 42):
    """
    Create a heatmap showing distance to goal from every position.

    Args:
        seed: Random seed for reproducibility
    """
    print("=" * 70)
    print("MANHATTAN DISTANCE HEATMAP")
    print("=" * 70)
    print("Shows Manhattan distance to goal from each position")
    print()

    env = GridEnvironment(obstacle_density=0.15, seed=seed)
    perception = RobotPerception(env)
    goal_pos = env.get_goal_position()
    start_pos = env.get_start_position()

    print("Legend: * = Goal, S = Start, # = Obstacle, . = Distance value")
    print()

    # Create heatmap
    for x in range(env.GRID_SIZE):
        for y in range(env.GRID_SIZE):
            if (x, y) == goal_pos:
                print("*", end=" ")
            elif (x, y) == start_pos:
                print("S", end=" ")
            elif (x, y) in env.get_obstacles():
                print("#", end=" ")
            else:
                distance = perception.calculate_manhattan_distance(
                    (x, y), goal_pos)
                print(distance, end=" ")
        print()

    print()


def motion_patterns(seed: int = 42):
    """
    Analyze the movement patterns from a successful run.

    Args:
        seed: Random seed for reproducibility
    """
    print("=" * 70)
    print("MOVEMENT PATTERN ANALYSIS")
    print("=" * 70)
    print()

    env = GridEnvironment(obstacle_density=0.15, seed=seed)
    simulation = RobotSimulation(env)
    results = simulation.run(verbose=False)

    if not results['success']:
        print("Simulation did not succeed. Skipping pattern analysis.")
        print()
        return

    # Analyze direction changes
    history = results['movement_history']
    direction_map = {
        (-1, 0): 'UP',
        (1, 0): 'DOWN',
        (0, -1): 'LEFT',
        (0, 1): 'RIGHT'
    }

    directions = []
    for i in range(1, len(history)):
        prev = history[i-1]
        curr = history[i]
        dx = curr[0] - prev[0]
        dy = curr[1] - prev[1]
        direction = direction_map.get((dx, dy), 'UNKNOWN')
        directions.append(direction)

    # Count direction usage
    from collections import Counter
    direction_counts = Counter(directions)

    print("Direction Usage:")
    print("─" * 40)
    total = len(directions)
    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        count = direction_counts.get(direction, 0)
        percentage = 100 * count / total if total > 0 else 0
        bar = "█" * int(percentage / 5)
        print(f"{direction:6s} {count:3d} ({percentage:5.1f}%) {bar}")

    print()


def main():
    """Run visualization and analysis examples."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " ROBOT GRID NAVIGATION - VISUALIZATION & ANALYSIS TOOLS ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    # Run analyses
    analyze_single_run(seed=42)
    compare_obstacle_densities(seeds=5)
    compare_seeds(num_seeds=10, density=0.15)
    perception_heatmap(seed=42)
    motion_patterns(seed=42)

    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
