#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from TestMethod import *

def updateCells(self, robot, distance, ui):
    return cUpdateCells(self, robot, distance, ui)

cdef cUpdateCells(self, robot, distance, ui):
    """
    Updates the cells within the Occupancy Map using the Distance measurements from the Robot Scan either through
    the physical sensors or the simulated map. Returns a list of cells_to_be_updated.
    """

    cdef:
        int angle
        float robot_origin_world_x, robot_origin_world_y, robot_origin_world_deg
        float end_of_seg_world_x, end_of_seg_world_y

    robot_origin_world_x, robot_origin_world_y, robot_orientation_deg = robot.robot_position_in_world
    self.max_range = robot.max_range
    self.row_size, self.col_size = [ui.row_size, ui.col_size]
    self.world_width, self.world_height = [ui.world_width, ui.world_height]
    
    self.cells_that_changed = []

    self.ui = ui

    for angle in range(360):
        if distance[angle] < robot.max_range:
            obstacle_is_sensed = True
        else:
            obstacle_is_sensed = False

        end_of_seg_world_x = findXPrime(robot_origin_world_x, distance[angle], angle)
        end_of_seg_world_y = findYPrime(robot_origin_world_y, distance[angle], angle)

        end_of_seg_world_x = max(end_of_seg_world_x, -self.world_width)
        end_of_seg_world_x = min(end_of_seg_world_x, self.world_width)

        #if end_of_seg_world_x <= -self.world_width:
        #    end_of_seg_world_x = -self.world_width + 1
        #elif end_of_seg_world_x >= self.world_width:
        #    end_of_seg_world_x  = self.world_width - 1

        end_of_seg_world_y = max(end_of_seg_world_y, -self.world_height)
        end_of_seg_world_y = min(end_of_seg_world_y, self.world_height)

        #if end_of_seg_world_y <= -self.world_height:
        #    end_of_seg_world_y = -self.world_height + 1
        #elif end_of_seg_world_y >= self.world_height:
        #    end_of_seg_world_y = self.world_height - 1

        findCellOccupancy(self,
                          [end_of_seg_world_x, end_of_seg_world_y],
                          distance[angle],
                          obstacle_is_sensed,
                          robot.robot_position_in_world)

    return self.cells_that_changed

cdef float findCellOccupancy(self,
                              end_of_seg_in_world,
                              current_distance_measurement,
                              obstacle_is_sensed,
                              robot_position):
    """
    Finds occupancy of the cells that occupy the line segment from the origin to the end point
    """

    cdef:
        int cell_steps
        float robot_origin_world_x, robot_origin_world_y, robot_origin_world_deg, run_of_segment, rise_of_segment
        float end_of_seg_world_x, end_of_seg_world_y, x_steps, y_steps

    robot_origin_world_x, robot_origin_world_y, robot_orientation_deg = robot_position
    end_of_seg_world_x, end_of_seg_world_y = end_of_seg_in_world

    run_of_segment = end_of_seg_world_x - robot_origin_world_x
    rise_of_segment = end_of_seg_world_y - robot_origin_world_y

    # Check for Limits
    if abs(run_of_segment) < 0.1:
        run_of_segment = 0

    if abs(rise_of_segment) < 0.1:
        rise_of_segment = 0

    # The cell steps are the maximum number of steps from the origin to the end point in world coords and grid denoms.
    cell_steps = int(round(max(abs(rise_of_segment / self.row_size), abs(run_of_segment / self.col_size))))

    x_steps = run_of_segment / float(cell_steps)
    y_steps = rise_of_segment / float(cell_steps)

    # Check for limits and negate the steps in case the steps are not in the positive direction
    if abs(x_steps) > self.col_size:
        x_steps = self.col_size

        if run_of_segment < 0:
            x_steps *= -1

    if abs(y_steps) > self.row_size:
        y_steps = self.row_size

        if rise_of_segment < 0:
            y_steps *= -1

    # Set current world location being tested as the origin
    current_location_in_world_x = robot_origin_world_x
    current_location_in_world_y = robot_origin_world_y

    # If the origin cell is occupied, set that cell and return to calling method
    if cell_steps == 0:
        setCellPOcc(self, end_of_seg_in_world, current_distance_measurement, True, robot_position)
        return 0

    # Process cells leading up to the end point
    cdef int step

    for step in range(cell_steps):
        current_location_in_world_x += x_steps
        current_location_in_world_y += y_steps
        setCellPOcc(self, [current_location_in_world_x, current_location_in_world_y], current_distance_measurement, False, robot_position)
        #cSetCellPOcc([current_location_in_world_x, current_location_in_world_y], current_distance_measurement, False, robot_position)

    # Process end point cell
    setCellPOcc(self, end_of_seg_in_world, current_distance_measurement, obstacle_is_sensed, robot_position)

cdef float setCellPOcc(self, current_position, current_distance_measurement, obstacle_is_sensed, robot_position):
    """
    Sets the cell passed with a P(occ) given the evidence being whether it is occupied and the prior knowledge of its
    status.
    """

    cdef:
        int cell_idx
        float robot_origin_world_x, robot_origin_world_y, robot_origin_world_deg
        float current_grid_location_x, current_grid_location_y, prior_occ, inv_prior, POcc, PEmp, probability

    robot_origin_world_x, robot_origin_world_y, robot_orientation_deg = robot_position
    current_position_world_x, current_position_world_y = current_position

    current_grid_location_x, current_grid_location_y = self.ui.screenToGrid(
        self.ui.worldToScreen(current_position))

    if current_grid_location_x >= self.num_cols:
        current_grid_location_x = self.num_cols - 1
    elif current_grid_location_x < 0:
        current_grid_location_x = 0

    if current_grid_location_y >= self.num_rows:
        current_grid_location_y = self.num_rows - 1
    elif current_grid_location_y < 0:
        current_grid_location_y = 0

    cell_idx = current_grid_location_y * self.num_cols + current_grid_location_x
    prior_occ = self.occ_map_cell[cell_idx]["P(occ)"]
    
    # Inverse the probability of the prior
    if prior_occ is None:
        prior_occ = 0.5
    inv_prior = 1.0 - prior_occ

    # Get new probabilities
    if current_distance_measurement < self.max_range:
        POcc = self.max_occupied * ((self.max_range - float(current_distance_measurement)) / self.max_range)
        PEmp = self.max_empty * ((self.max_range - float(current_distance_measurement)) / self.max_range)
    else:
        return prior_occ

    # Calculate Bayesian probability
    if obstacle_is_sensed is True:
        probability = (POcc * prior_occ) / ((POcc * prior_occ) + (PEmp * inv_prior))
    else:
        probability = (PEmp * prior_occ) / ((PEmp * prior_occ) + (POcc * inv_prior))

    # print prior_occ, probability

    if probability != prior_occ:
        if probability > 0.5:
            # print "Above", probability
            self.occ_map_cell[cell_idx]["colour"] = "Grey" + str(int((1-probability) * 100))
        elif probability < 0.5:
            # print "Below", probability
            self.occ_map_cell[cell_idx]["colour"] = "Grey" + str(int((1-probability) * 100))
        elif probability == 0.5:
            self.occ_map_cell[cell_idx]["colour"] = "Grey50"

        self.cells_that_changed.append(cell_idx)

    self.occ_map_cell[cell_idx]["P(occ)"] = probability