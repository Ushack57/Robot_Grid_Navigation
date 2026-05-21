"""
Main Entry Point for Robot Grid Navigation Simulation

Demonstrates the complete robot navigation system with:
- Grid environment with obstacles
- Robot perception and decision-making
- Step-by-step simulation
- Results visualization
"""

from grid_environment import GridEnvironment
from simulation import RobotSimulation


def main():
    """Run the robot navigation simulation."""

    # Create environment with 20% obstacle density
    print("Creating environment...\n")
    environment = GridEnvironment(obstacle_density=0.2, seed=42)

    # Create simulation
    simulation = RobotSimulation(environment)

    # Run simulation
    results = simulation.run(verbose=True)

    # Display path visualization
    print("\n" + "=" * 60)
    print("PATH VISUALIZATION")
    print("=" * 60 + "\n")
    print(simulation.visualize_path())

    # Display detailed movement log
    print("=" * 60)
    print("DETAILED MOVEMENT LOG")
    print("=" * 60 + "\n")

    if results['movement_log']:
        for entry in results['movement_log'][:15]:  # Show first 15 steps
            print(f"Step {entry['step']:3d}: {entry['from_position']} → " +
                  f"{entry['to_position']} " +
                  f"({entry['direction']:6s}) | " +
                  f"Distance to goal: {entry['distance_to_goal']}")

        if len(results['movement_log']) > 15:
            print(f"\n... ({len(results['movement_log']) - 15} more steps)")

    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Steps: {results['steps_taken']}")
    print(f"Distance Traveled: {results['robot_stats']['distance_traveled']}")
    print(f"Path Efficiency: {results['robot_stats']['distance_traveled'] / max(results['steps_taken'], 1):.2f} " +
          f"(distance per step)")
    print(f"Start: {results['robot_stats']['start_position']}")
    print(f"End: {results['final_position']}")
    print(f"Goal: {results['goal_position']}")
    print("=" * 60 + "\n")


def run_multiple_simulations(num_runs: int = 5):
    """
    Run multiple simulations with different random seeds.

    Args:
        num_runs: Number of simulations to run
    """
    print(f"\nRunning {num_runs} simulations with different seeds...\n")

    success_count = 0
    total_steps = 0
    step_list = []

    for run in range(num_runs):
        print(f"\n{'='*60}")
        print(f"SIMULATION {run + 1}/{num_runs}")
        print(f"{'='*60}\n")

        # Create environment with different seed
        environment = GridEnvironment(obstacle_density=0.2, seed=run)
        simulation = RobotSimulation(environment)

        # Run simulation without verbose output
        results = simulation.run(verbose=False)

        status = "✓ SUCCESS" if results['success'] else "✗ FAILED"
        print(f"{status}: Steps = {results['steps_taken']}, " +
              f"Final Distance = {results['distance_to_goal']}")

        if results['success']:
            success_count += 1

        total_steps += results['steps_taken']
        step_list.append(results['steps_taken'])

    # Print summary
    print(f"\n{'='*60}")
    print("MULTI-RUN SUMMARY")
    print(f"{'='*60}")
    print(
        f"Success Rate: {success_count}/{num_runs} ({100*success_count/num_runs:.1f}%)")
    print(f"Average Steps: {total_steps/num_runs:.1f}")
    print(f"Min Steps: {min(step_list)}")
    print(f"Max Steps: {max(step_list)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Run single simulation
    main()

    # Uncomment the line below to run multiple simulations
    # run_multiple_simulations(5)
