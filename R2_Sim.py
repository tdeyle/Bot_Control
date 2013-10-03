#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = "Theo Deyle"
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

# A simulator/GUI that simulates the use of a Neato LDS attached to a robot.
# Features:
# - see individual probabilities of the cells
# - add and remove obstacles on the fly
# - detect features like corners, walls and doors
# - localize within completed map
# - plan path with starting and ending positions
# - sonar sensors implemented into different windows along with a different window for the LDS
# Distance readings come from dummy data, or directly from LDS. This is selectable by button in GUI. This feature will
# also enable/disable remote operation of bot.
# TODO: Convert everything to Cython

from Map_Sim import *
from Occ_Map import *
#from Robot_Control import *
from Robot_Control_cy import *
from UI import *
from swampy.Lumpy import Lumpy
from time import *

# Setup variables
window_size = [1200, 600]
world_size = [12000, 6000]
grid_size = [50,50]
max_range = 6000
robot_width = 457
robot_colour = "blue"
wheel_colour = "black"

sim = True

R2 = Robot(max_range, robot_width)
ui_window = Window(world_size, grid_size, window_size, robot_colour, wheel_colour,  "R2D2 Simulation")
occupancy_map = OccupancyMap(R2, ui_window)

if sim:
    sim_map= Map(world_size, grid_size)
else:
    sim_map = None

R2.set_position(0,0,0)
robot_position_world = [0,0,0]
robot_position_screen = ui_window.worldToScreen([robot_position_world[0], robot_position_world[1]])

ui_window.bindButtons(R2, ui_window, sim_map, occupancy_map)

# ----Test Code below----
if sim:
    distance = R2.scan(ui_window,
                    sim_map)

# Initial Scanning
t1 = time()
print "Checking probs.."
cells_to_change = occupancy_map.updateProbabilities(R2, distance, ui_window)
t2 = time()
print "...Done", t2-t1

# Initial Updating
t1 = time()
print "Updating Map..."
ui_window.updateMap(cells_to_change, occupancy_map.occ_map_cell)
t2 = time()
print "...Done", t2-t1

t1 = time()
print "Drawing Bot..."
ui_window.drawRobot([robot_position_world[0],
                                    robot_position_world[1],
                                    robot_position_world[2]],
                                   R2.robot_body_width,
                                   R2.robot_body_length,
                                   R2.robot_wheel_length,
                                   R2.robot_wheel_width)
t2 = time()
print "...Done", t2-t1

t1 = time()
print "Drawing Laser"
ui_window.drawLaser(distance)
t2 = time()
print "...Done", t2-t1

ui_window.top.mainloop()