#!/bin/bash

# Execution permissions
chmod +x scripts/auto_drive.py
chmod +x scripts/avoid_obstacles.py
chmod +x scripts/bumper_halter.py
chmod +x scripts/controller.py
chmod +x scripts/manual_nav.py
chmod +x scripts/periodic_turn.py

# Launch project
roslaunch project1 project1.launch