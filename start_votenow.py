#!/usr/bin/env python3
"""
VoteNow Application Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    frontend_dir = script_dir / "voting-frontend"
    
    print("🗳️  VoteNow Application Startup")
    print("=" * 40)
    
    # Check if the frontend directory exists
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return 1
    
    # Change to the frontend directory
    os.chdir(frontend_dir)
    print(f"📁 Working directory: {frontend_dir}")
    
    # Check if requirements.txt exists
    requirements_file = frontend_dir / "requirements.txt"
    if requirements_file.exists():
        print("📦 Installing/checking dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Warning: Could not install some dependencies")
    
    # Start the Flask application
    print("🚀 Starting VoteNow application...")
    print("📍 Application will be available at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the application")
    print("=" * 40)
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 VoteNow application stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
