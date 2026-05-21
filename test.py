"""
Test script to verify all components of the Robot Grid Navigation System

Tests:
1. Grid environment creation
2. Robot movement
3. Perception module
4. Decision-making engine
5. Complete simulation with multiple runs
"""

from grid_environment import GridEnvironment
from robot import Robot
from perception import RobotPerception
from decision_making import DecisionMaker
from simulation import RobotSimulation


def test_grid_environment():
    """Test grid environment functionality."""
    print("=" * 60)
    print("TEST 1: Grid Environment")
    print("=" * 60)

    env = GridEnvironment(obstacle_density=0.15, seed=42)
    print(f"✓ Grid created: {env}")
    print(f"✓ Start: {env.get_start_position()}")
    print(f"✓ Goal: {env.get_goal_position()}")
    print(f"✓ Obstacles: {len(env.get_obstacles())}")
    print(f"✓ Valid position (0,0): {env.is_valid_position(0, 0)}")
    print(f"✓ Valid position (1,1): {env.is_valid_position(1, 1)}")
    print("\n" + env.visualize((0, 0)))
    print()


def test_robot():
    """Test robot movement."""
    print("=" * 60)
    print("TEST 2: Robot Movement")
    print("=" * 60)

    robot = Robot((0, 0))
    print(f"✓ Robot created at {robot.get_position()}")

    # Test movements
    robot.move('DOWN')
    print(f"✓ After DOWN: {robot.get_position()} (expected: (1, 0))")

    robot.move('RIGHT')
    print(f"✓ After RIGHT: {robot.get_position()} (expected: (1, 1))")

    robot.move('RIGHT')
    print(f"✓ After RIGHT: {robot.get_position()} (expected: (1, 2))")

    print(f"✓ Movement history: {robot.get_movement_history()}")
    print(f"✓ Total moves: {robot.get_moves_count()}")
    print()


def test_perception():
    """Test perception module."""
    print("=" * 60)
    print("TEST 3: Robot Perception")
    print("=" * 60)

    env = GridEnvironment(obstacle_density=0.15, seed=42)
    perception = RobotPerception(env)

    pos = (2, 2)
    print(f"✓ Testing from position: {pos}")

    valid_moves = perception.get_valid_moves(pos)
    print(f"✓ Valid moves: {valid_moves}")

    obstacles = perception.detect_obstacles(pos)
    print(f"✓ Obstacles detected: {obstacles}")

    goal_pos = perception.locate_goal(pos)
    print(f"✓ Goal location: {goal_pos}")

    distance = perception.calculate_manhattan_distance(pos, goal_pos)
    print(f"✓ Distance to goal: {distance}")
    print()


def test_decision_making():
    """Test decision-making engine."""
    print("=" * 60)
    print("TEST 4: Decision Making")
    print("=" * 60)

    env = GridEnvironment(obstacle_density=0.15, seed=42)
    perception = RobotPerception(env)
    decision_maker = DecisionMaker(perception)

    pos = (2, 2)
    print(f"✓ Testing from position: {pos}")

    best_move = decision_maker.get_best_move(pos)
    print(f"✓ Best move: {best_move}")

    ranked_moves = decision_maker.get_best_moves_ranked(pos)
    print(f"✓ Ranked moves: {ranked_moves}")

    can_move, direction = decision_maker.make_decision(pos)
    print(f"✓ Can move: {can_move}, Direction: {direction}")

    decision_info = decision_maker.get_decision_info(pos)
    print(f"✓ Decision info keys: {list(decision_info.keys())}")
    print()


def test_single_simulation(obstacle_density=0.15, seed=42):
    """Test single simulation."""
    print("=" * 60)
    print(
        f"TEST 5: Single Simulation (density={obstacle_density}, seed={seed})")
    print("=" * 60)

    env = GridEnvironment(obstacle_density=obstacle_density, seed=seed)
    simulation = RobotSimulation(env)
    results = simulation.run(verbose=False)

    status = "✓ SUCCESS" if results['success'] else "✗ FAILED"
    print(f"{status}")
    print(f"  Steps: {results['steps_taken']}")
    print(f"  Final pos: {results['final_position']}")
    print(f"  Goal: {results['goal_position']}")
    print(f"  Distance: {results['distance_to_goal']}")

    if results['success']:
        print(f"\n✓ Path found!")
        print(f"  Path length: {len(results['movement_history'])}")
    else:
        print(f"\n✗ No path found")
        if results['max_steps_exceeded']:
            print(f"  Reason: Max steps exceeded")
        else:
            print(f"  Reason: Robot got stuck")

    print()
    return results['success']


def test_multiple_simulations(num_runs=5):
    """Test multiple simulations with different seeds."""
    print("=" * 60)
    print(f"TEST 6: Multiple Simulations ({num_runs} runs)")
    print("=" * 60)

    success_count = 0
    results_list = []

    for i in range(num_runs):
        env = GridEnvironment(obstacle_density=0.15, seed=i)
        simulation = RobotSimulation(env)
        results = simulation.run(verbose=False)

        success = results['success']
        steps = results['steps_taken']
        distance = results['distance_to_goal']

        status = "✓" if success else "✗"
        print(
            f"  Run {i+1}: {status} Success={success}, Steps={steps}, Distance={distance}")

        if success:
            success_count += 1

        results_list.append(results)

    print(f"\n✓ Summary:")
    print(
        f"  Success rate: {success_count}/{num_runs} ({100*success_count/num_runs:.1f}%)")

    successful_runs = [r for r in results_list if r['success']]
    if successful_runs:
        avg_steps = sum(r['steps_taken']
                        for r in successful_runs) / len(successful_runs)
        print(f"  Average steps (successful): {avg_steps:.1f}")

    print()


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " ROBOT GRID NAVIGATION - COMPREHENSIVE TEST SUITE ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Run individual component tests
    test_grid_environment()
    test_robot()
    test_perception()
    test_decision_making()

    # Run simulation tests
    test_single_simulation(obstacle_density=0.15, seed=42)
    test_single_simulation(obstacle_density=0.1, seed=123)
    test_multiple_simulations(num_runs=10)

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    print()


if __name__ == "__main__":
    run_all_tests()
