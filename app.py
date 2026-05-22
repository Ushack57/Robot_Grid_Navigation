"""
Flask Web Application for Robot Grid Navigation Visualization

Provides a professional web interface for:
- Interactive grid visualization
- Step-by-step robot animation
- Run button for new simulations
- Real-time statistics and information
"""

from flask import Flask, render_template, jsonify, request
from core import GridEnvironment, RobotSimulation
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Store current simulation state
current_simulation = None
current_results = None


@app.route('/')
def index():
    """Render the main visualization page."""
    return render_template('index.html')


@app.route('/api/new-simulation', methods=['POST'])
def new_simulation():
    """
    Create a new simulation with random obstacles.

    Request JSON:
    {
        "obstacle_density": float (0.0-1.0),
        "seed": int or null (null for random)
    }
    """
    global current_simulation, current_results

    try:
        data = request.json
        obstacle_density = data.get('obstacle_density', 0.15)
        seed = data.get('seed', None)

        # Create environment and simulation
        env = GridEnvironment(obstacle_density=obstacle_density, seed=seed)
        current_simulation = RobotSimulation(env)

        # Run simulation to get complete data
        current_results = current_simulation.run(verbose=False)

        # Prepare response
        response = {
            'success': True,
            'grid_size': env.GRID_SIZE,
            'start_pos': env.get_start_position(),
            'goal_pos': env.get_goal_position(),
            'obstacles': list(env.get_obstacles()),
            'simulation_success': current_results['success'],
            'total_steps': current_results['steps_taken'],
            'movement_history': current_results['movement_history'],
            'final_position': current_results['final_position'],
            'distance_to_goal': current_results['distance_to_goal']
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/simulation-data', methods=['GET'])
def simulation_data():
    """Get current simulation data for visualization."""
    global current_results

    if current_results is None:
        return jsonify({
            'success': False,
            'error': 'No simulation running'
        }), 400

    return jsonify({
        'success': True,
        'movement_history': current_results['movement_history'],
        'obstacles': current_results['robot_stats'],
        'final_position': current_results['final_position'],
        'goal_position': current_results['goal_position'],
        'simulation_success': current_results['success'],
        'total_steps': current_results['steps_taken'],
        'distance_traveled': current_results['robot_stats']['distance_traveled']
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics from current simulation."""
    global current_results, current_simulation

    if current_results is None:
        return jsonify({
            'success': False,
            'error': 'No simulation running'
        }), 400

    stats = {
        'success': True,
        'simulation_success': current_results['success'],
        'steps_taken': current_results['steps_taken'],
        'path_length': len(current_results['movement_history']),
        'distance_traveled': current_results['robot_stats']['distance_traveled'],
        'start_position': current_results['robot_stats']['start_position'],
        'final_position': current_results['final_position'],
        'goal_position': current_results['goal_position'],
        'distance_to_goal': current_results['distance_to_goal'],
        'obstacle_count': len(current_simulation.environment.get_obstacles()),
        'total_cells': current_simulation.environment.GRID_SIZE ** 2
    }

    if current_results['steps_taken'] > 0:
        stats['efficiency'] = current_results['robot_stats']['distance_traveled'] / \
            current_results['steps_taken']
    else:
        stats['efficiency'] = 0

    return jsonify(stats)


if __name__ == '__main__':
    # Run Flask development server
    app.run(debug=True, port=5000, host='127.0.0.1')
