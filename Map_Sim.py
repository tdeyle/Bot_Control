#!/usr/bin/env python

__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from math import *
from UI import *

class Map:
    def __init__(self,
                 world_size,
                 grid_size):
        """
        Setup the initial simulated map with an occupancy of zero.

        :param world_size: Passes the world size into module -> Width x Height in mm
        :param grid_size: Passes the grid size into module -> Width x Height in mm
        :param window_size: Passes the window size into module -> Width x Height in px
        :param max_range: Passes the max range of the laser sensor
        """
        # TODO: Do we need this many variables? Or can they be moved into the UI.py module?

        self.world_width, self.world_height = world_size
        self.grid_width, self.grid_height = grid_size

        self.num_rows = self.world_height / self.grid_height
        self.num_cols = self.world_width / self.grid_width

        self.cell = [0 for i in range(self.num_rows*self.num_cols)]

        self.layoutWalls()

    def layoutWalls(self):

        # for i in range(self.num_columns):
        #     self.cell[i] = 1
        #     self.cell[(self.num_rows * self.num_columns - self.num_columns) + i] = 1
        #
        # for i in range(self.num_rows):
        #     self.cell[self.num_columns * i] = 1
        #     self.cell[(self.num_columns * i) + self.num_columns - 1] = 1

        for cell_xpos in range(self.num_rows):
                for cell_ypos in range(self.num_cols):
                    if cell_xpos <= 1 or \
                                    cell_xpos >= (self.num_rows - 2) or \
                                    cell_ypos <= 1 or \
                                    cell_ypos >= (self.num_cols - 2):
                        idx = cell_xpos * self.num_cols + cell_ypos
                        self.cell[idx] = 1

    def layoutObstacles(self):

        """

        Layout obstacles on the map, updating the cells of the map
        """
        pass

    def layoutRooms(self, width, height, origin, door=False):

        """

        Layout room within the world, updates the cells of the current map.

        :param width: Width of the room in mm (World Size)
        :param height: Height of the room in mm (World Size)
        :param origin: Upper right location in world coordinates.
        :param door: Whether a door is found on one of the walls. Boolean
        """
        pass

    def getMap(self):
        """

        This will return the map of cells in a list of integers.

        :return: list of integers
        """
        return self.cell

    def getRowsColumns(self):
        """
        This will return the number of rows and number of columns when called.

        :return: integers
        """
        return self.num_rows, self.num_cols

    def checkMap(self):
        """

        This prints the completed map formatted by the number of columns and rows.
        """

        for i in range(self.num_rows):
            print self.cell[(self.num_cols * i):((i * self.num_cols) + self.num_cols)]

if __name__ == '__main__':
    window_size = [1200, 600]
    world_size = [12000, 6000]
    grid_size = [50,50]
    max_range = 6000


    test = Map(world_size, grid_size, window_size, max_range)
    win = Window(world_size, grid_size, window_size, "Testing the simMap")

    robot_position = win.worldToScreen([0,0])

    num_rows, num_cols = test.getRowsColumns()
    distance = test.scan(0,0,0) #robot_position[0], robot_position[1], 0)
    current_map = test.getMap()
    win.drawRobot([robot_position[0], robot_position[1], 0])
    win.drawLaser(distance)

    win.top.mainloop()
