#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from UI import *
from Occ_Map_Utilities_cy import *
#from Occ_Map_Utilities import *
#from numpy import *

class OccupancyMap:
    """
    Draws and updates a map that represents the probability of occupancy within a world.
    - Able to display an overlay showing obstacles and map
    - Uses a change cell list to change only the cells in that list, speeding processing
    - Draws a representation of robot onto map
    - Determine features based on laser output and highlight them
    - Setup in Pure Python and calls a Cython method to perform calculations
    """

    def __init__(self,
                 robot,
                 ui):

        self.num_cols = ui.world_width / ui.col_size
        self.num_rows = ui.world_height / ui.row_size

        # Variables for P(occupancy)
        self.unoccupied = 0.0
        self.occupied = 1.0
        self.unknown = 0.5

        # Variables for setting a dynamic obstacle ! Not implemented yet
        self.dynamic_amount = 1
        self.dynamic_limit = 50
        self.dynamic_cell_threshold = 0.4

        self.off = False
        self.on = True

        self.overlay_on = False

        self.colour_unocc = "White"
        self.colour_occ = "Black"
        self.colour_unknown = "Grey50"

        self.max_occupied = 0.91
        self.max_empty = 0.1

        self.occ_map_cell = {}
        self.cells_that_changed = []

        for row in range(self.num_rows):
            for column in range(self.num_cols):
                idx = row * self.num_cols + column
                screen_location = ui.gridToScreen([row,column])
                self.occ_map_cell[idx] = {"colour": self.colour_unknown,
                                          "P(occ)": self.unknown,
                                          "Prior(occ)": self.unknown,
                                          "Row_Number": row,
                                          "Col_Number": column,
                                          "screen_point_x": screen_location[0],
                                          "screen_point_y": screen_location[1],
                                          "Occupied?": 0,
                                          "Dynamic?": 0,
                                          "Type": "unknown",
                                          "Scanned": 0}

        ui.drawMap(self.occ_map_cell)


    def updateProbabilities(self, robot, distance, ui):
        """
        Takes the list of values in the distance parameter and calculates the probabilities of the cells that are
        affected. It appends the cells changes to the cell_changes list and calls the updateMap method in the UI
        module.

        :param distance: list of integers that represent the distance readings taken by the robot.
        """

        return updateCells(self, robot, distance, ui)

if __name__ == '__main__':
    test = OccupancyMap((800, 600), (50,50), (800,600), title="Test from Occ_Map")
    test.sim_window.top.mainloop()