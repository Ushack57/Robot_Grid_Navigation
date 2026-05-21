#!/usr/bin/env python3
"""
Robot Grid Navigation - Web Visualizer Launcher

This script starts the Flask web server with automatic dependency checking.
"""

import subprocess
import sys
import os


def check_python():
    """Check if Python version is 3.7 or higher."""
    if sys.version_info < (3, 7):
        print("✗ Error: Python 3.7 or higher required")
        print(f"  Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} found")
    return True


def check_flask():
    """Check if Flask is installed, install if not."""
    try:
        import flask
        print(f"✓ Flask {flask.__version__} found")
        return True
    except ImportError:
        print("⚠ Flask not installed. Installing now...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install',
                'Flask==2.3.0', 'Werkzeug==2.3.0', '-q'
            ])
            print("✓ Flask installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install Flask")
            return False


def start_server():
    """Start the Flask development server."""
    print()
    print("╔" + "=" * 60 + "╗")
    print("║" + " Robot Grid Navigation - Web Visualizer ".center(60) + "║")
    print("╚" + "=" * 60 + "╝")
    print()
    print("🚀 Starting Flask server...")
    print()
    print("📱 Open your browser and navigate to:")
    print()
    print("   ► http://localhost:5000")
    print()
    print("⌨️  Press Ctrl+C to stop the server")
    print()
    print("=" * 62)
    print()

    try:
        from app import app
        app.run(debug=True, port=5000, host='127.0.0.1')
    except KeyboardInterrupt:
        print()
        print()
        print("⏹️  Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print()
    print("╔" + "=" * 60 + "╗")
    print("║" + " Robot Grid Navigation Setup ".center(60) + "║")
    print("╚" + "=" * 60 + "╝")
    print()

    # Check Python
    if not check_python():
        sys.exit(1)

    # Check Flask
    if not check_flask():
        sys.exit(1)

    print()

    # Start server
    start_server()


if __name__ == '__main__':
    main()
