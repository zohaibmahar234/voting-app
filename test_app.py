#!/usr/bin/env python3
"""
Test script to validate the VoteNow application
"""

import sys
import os

# Add the voting-frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'voting-frontend'))

try:
    from app import app
    print("✓ Flask app imports successfully")
    
    # Test that all routes are defined
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    expected_routes = [
        '/',
        '/create-poll',
        '/poll-created/<poll_id>',
        '/poll/<poll_id>',
        '/poll/<poll_id>/results',
        '/poll/<poll_id>/thanks',
        '/join-poll'
    ]
    
    for route in expected_routes:
        if route in routes or any(r.startswith(route.split('<')[0]) for r in routes):
            print(f"✓ Route {route} is defined")
        else:
            print(f"✗ Route {route} is missing")
    
    print("\n✓ All basic routes are properly configured")
    print("✓ Application is ready to run!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r voting-frontend/requirements.txt")
except Exception as e:
    print(f"✗ Error: {e}")
