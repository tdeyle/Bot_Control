#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from math import pi
from random import random

def move(window, robot, command):
    """
    Moves the robot by passing the proper command to the robot class.
    """

    move_step = robot.move_step
    turn_modifier = 1

    window.occmap_canvas.delete('R2')

    if command == 'Forward' or command == 'Reverse:':
        if command == 'Reverse':
            move_step = -move_step

        robot.move(0.0, move_step)

        if abs(robot.robot_position_in_world[0]) + robot.robot_body_length / 2 + robot.robot_wheel_length >= window.world_width / 2 or \
            abs(robot.robot_position_in_world[1]) + robot.robot_body_length / 2 + robot.robot_wheel_length >= window.world_height / 2:
            print "Hit a wall"
            robot.move(0.0, -move_step)

        print "Moving ", command, "by", move_step, robot.robot_position_in_world

    elif command == 'Turn Right' or command == 'Turn Left':
        print command
        if command == 'Turn Right':
            turn_modifier = -1
        robot.set_position(robot.robot_position_in_world[0],
                           robot.robot_position_in_world[1],
                           robot.robot_position_in_world[2] + (pi * turn_modifier) / 16.0)

    window.drawRobot(robot.robot_position_in_world,
                     robot.robot_body_width,
                     robot.robot_body_length,
                     robot.robot_wheel_length,
                     robot.robot_wheel_width)

def scan_and_update(robot, window, sim_map, occ_map):
    """
    Issues the scan command to the robot, updates the occupancy map, and redraws the screen.
    """

    print "Scanning started..."

    distance = robot.scan(window, sim_map)
    cells_to_change = occ_map.updateProbabilities(robot, distance, window)
    window.updateMap(cells_to_change, occ_map.occ_map_cell)
    window.drawRobot(robot.robot_position_in_world,
                     robot.robot_body_width,
                     robot.robot_body_length,
                     robot.robot_wheel_length,
                     robot.robot_wheel_width)

    print "Scanning Finished"

def change_move_step(robot, step_amount):
    """
    Changes the rate to which the robot moves when a single press of the button is made.
    """

    robot.move_step += step_amount
    print "Move step changed to: ", robot.move_step

def toggle_overlay(self):
    """

    """
    pass

def place_obstacle(event, remove_flag, mouse_flag, window, occ_map):
    """
python -m cProfile R2_Sim.py -o your_script.profile
    """

    changes = []

    print "Placing Obstacle @:", event.x, event.y, "..."

    x = int((event.x / window.world_to_screen_x) / window.col_size)
    y = int((event.y / window.world_to_screen_y) / window.row_size)

    seed = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]]

    for j in range(5):
        for k in range(5):
            idx = (y + j) * window.num_cols + (x + k)
            if remove_flag == 0:
                occ_map.occ_map_cell[idx]["Occupied?"] = 1
            else:
                occ_map.occ_map_cell[idx]["Occupied?"] = 0

            changes.append(idx)

            print changes, occ_map[changes]["screen_point_x"]

            window.updateMap(changes, occ_map)

def check_probability_of_cell(self):
    """

    """
    pass

