#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

# TODO: This will be where control to the bot and the particles will be:
    #  Movements
    #  Sensing
    #     Laser
    #     Sonar
    #     IR Sensors
    #     etc.
    #  Sizes

from math import sin, cos, pi, radians
#from numpy import *
from time import *
from TestMethod import *

class Robot:
    def __init__(self,
                 max_range = 6000,
                 robot_body_width = 457):

        self.robot_body_width = robot_body_width
        self.robot_body_length = self.robot_body_width
        self.robot_wheel_length = 0.4 * self.robot_body_width
        self.robot_wheel_width = 0.5 * self.robot_wheel_length
        self.max_range = max_range

        self.move_step = 10

        self.robot_position_in_world = [0, 0, 0]

    def scan(self,
             ui_param,
             sim_map):
        """
        Performs a scan with the center being the robot_x and robot_y locations and returns a list of distance values.

        :rtype : object
        :param robot_x: Location of Robot on X-Axis in World Coordinates (Center Origin)
        :param robot_y: Location of Robot on Y-Axis in World Coordinates (Center Origin)
        :param robot_orientation: Orientation of Robot in degrees in relation to "East" vector in World
        :return distance: list of values in mm that coincide with the distance between obstacles and the robot
        """

        # TODO: List all types.
        # TODO: Provide a method for scanning inside the TestMethod.pyx module

        time2 = time()

        print "Scan has started..."

        robot_x, robot_y, robot_orientation = self.robot_position_in_world

        distance = []

        cell = sim_map.cell

        for angle in range(360):
            local_angle = int((robot_orientation + angle) % 360.0)

            for length in range(self.max_range):
                x_prime = findXPrime(robot_x, length, local_angle)
                y_prime = findYPrime(robot_y, length, local_angle)

                screen_location_x = ui_param.window_width / 2 + x_prime * ui_param.world_to_screen_x
                screen_location_y = ui_param.window_height / 2 + y_prime * -ui_param.world_to_screen_y

                grid_x = int((screen_location_x / ui_param.world_to_screen_x) / ui_param.col_size)
                grid_y = int((screen_location_y / ui_param.world_to_screen_y) / ui_param.row_size)

                if grid_y >= ui_param.world_height / ui_param.row_size or \
                                grid_y <= 0 or \
                                grid_x >= ui_param.world_width / ui_param.col_size or \
                                grid_x <= 0:
                    # print "Hit the wall", length, "@", local_angle
                    distance.append(self.max_range - 1)
                    break
                elif cell[grid_y * ui_param.num_cols + grid_x] == 1:
                    # print length, "@", local_angle
                    distance.append(length)
                    break
                elif length == self.max_range - 1:
                    # print "Max_Distance reached"
                    distance.append(length)
        time1 = time()

        print "...Finished Scan: ", time1-time2

        return distance

    def scan_and_update(self):
        """

        """


    def set_position(self, new_x_world, new_y_world, new_orientation_rad):
        """
        Sets position of robot in world coordinates and radians
        """
        self.robot_position_in_world[0] = float(new_x_world)
        self.robot_position_in_world[1] = float(new_y_world)
        self.robot_position_in_world[2] = float(new_orientation_rad) % (2.0 * pi)
        print "Set", self.robot_position_in_world


    def move(self, steering_angle_in_rad, distance):
        """
        Moves robot by setting a new position with distance in world coords and radians
        """
        self.set_position(self.robot_position_in_world[0] + (distance * cos(self.robot_position_in_world[2])),
                          self.robot_position_in_world[1] + (distance * sin(self.robot_position_in_world[2])),
                          self.robot_position_in_world[2] + steering_angle_in_rad)

        print "Modified", self.robot_position_in_world

if __name__ == '__main__':
    a = Robot()

