#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

from Tkinter import *
from math import *
import UI_Commands as command
from UI_Utilities import *

class Window:

    def __init__(self, world_size, grid_size, window_size, robot_colour, wheel_colour, title=""):
        """
        Creates a window on the screen with separated frames for laser readout, global map and utility sides.
        :param world_size: size of the visible world that is represented by the UI, in mm.
        :param grid_size: size of the grid that divides the world, in mm
        :param window_size: size of the window that displays the UI, in px.
        :param title: of the window
        """

        # TODO: Add Keystroke and Mouse controls.

        self.top = Tk()

        self.window_width, self.window_height = window_size
        self.world_width, self.world_height = world_size
        self.col_size, self.row_size = grid_size

        self.laser_window_width = self.window_width
        self.laser_window_height = self.window_height/4

        self.sonar_window_width, self.sonar_window_height = [200, 200]

        self.origin = [self.window_width/2, self.window_height/2]

        # scale factor used in screen = world * scale
        self.world_to_screen_x = float(self.window_width) / float(self.world_width)
        self.world_to_screen_y = float(self.window_height) / float(self.world_height)

        self.num_rows = self.world_height / self.row_size
        self.num_cols = self.world_width / self.col_size

        # modifier that adds to the column/row during redraw/initial draw on the canvas
        self.row_offset = self.row_size * self.world_to_screen_x
        self.col_offset = self.col_size * self.world_to_screen_y

        window = Frame(self.top)
        window.pack()

        self.robot_colour = robot_colour
        self.wheel_colour = wheel_colour

        left_side = Frame(window)
        left_side.pack(side=LEFT)

        right_side = Frame(window)
        right_side.pack(side=TOP)

        #LeftSonar = Frame(right_side)
        #CenterSonar = Frame(right_side)
        #RightSonar = Frame(right_side)
        #LeftSonar.pack(fill=Y, side=TOP, expand=TRUE)
        #CenterSonar.pack()
        #RightSonar.pack()

        self.LeftSonar_canvas = Canvas(right_side,
                                       bg="Red",
                                       height=self.sonar_window_height,
                                       width=self.sonar_window_width)
        self.CenterSonar_canvas = Canvas(right_side,
                                       bg="Green",
                                       height=self.sonar_window_height,
                                       width=self.sonar_window_width)
        self.RightSonar_canvas = Canvas(right_side,
                                       bg="Purple",
                                       height=self.sonar_window_height,
                                       width=self.sonar_window_width)
        self.LeftSonar_canvas.pack()
        self.CenterSonar_canvas.pack()
        self.RightSonar_canvas.pack()

        occ_map = Frame(left_side)
        occ_map.pack(side=TOP, fill=BOTH)
        self.occmap_canvas = Canvas(occ_map, bg="grey", height=self.window_height, width=self.window_width)
        self.occmap_canvas.pack(fill=BOTH, expand=1)

        #options = Frame(right_side, height=self.window_height+self.window_height/4, width=self.window_width/4)
        #options.pack(side=RIGHT, fill=BOTH, expand=1)
        #
        #self.button1 = Button(options, text="Hi")
        #self.button1.grid(column=0, row=0, sticky="n")
        #self.entry1 = Entry(options)
        #self.entry1.grid(column=0, row=1, sticky="e")

        laserreadout = Frame(left_side)
        laserreadout.pack(side=BOTTOM)
        self.laserreadout_canvas = Canvas(laserreadout,
                                          bg="white",
                                          height=self.laser_window_height,
                                          width=self.laser_window_width)
        self.laserreadout_canvas.pack()

        self.top.wm_attributes("-topmost", 1)
        self.top.resizable(TRUE,TRUE)
        self.placeToCenter()
        self.top.title(title)

    def placeToCenter(self):
        """
        Centers the window in the center of the screen
        :param self:
        """

        # TODO: MAke this more readable

        ws = self.top.winfo_screenwidth()
        hs = self.top.winfo_screenheight()
        self.top.update_idletasks()
        w = self.top.winfo_reqwidth()
        h = self.top.winfo_reqheight()
        x = ws/2-w/2
        y = hs/2-h/2
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def worldToScreen(self, world_point):
        """
        Returns Screen Coordinate pair when given a World Coordinate pair

        :param world_point: (integer, integer)
        :return: (screen_point_x, screen_point_y)
        """

        return self.origin[0] + world_point[0] * self.world_to_screen_x, \
               self.origin[1] - world_point[1] * self.world_to_screen_y

    def screenToWorld(self, screen_point):
        """
        Returns World Coordinate pair when given a Screen Coordinate pair

        :param screen_point: (integer, integer)
        :return: (world_point_x, world_point_y)
        """

        return (screen_point[0] - self.origin[0]) / self.world_to_screen_x, \
               -(screen_point[1] - self.origin[1]) / self.world_to_screen_y

    def screenToGrid(self, screen_point):
        """
        Returns Grid Coordinate point when given a Screen Point Coordinate

        :param screen_point: (integer, integer)
        :return: (grid_point_x, grid_point_y)
        """

        return int((screen_point[0] / self.world_to_screen_x) / self.col_size), \
               int((screen_point[1] / self.world_to_screen_y) / self.row_size)

    def gridToScreen(self, grid_point):
        """
        Returns Screen Coordinate pair when given a Grid Coordinate pair

        :param grid_point: (integer, integer)
        :return: (screen_point_x, screen_point_y)
        """
        return grid_point[1] * self.col_size * self.world_to_screen_x, \
               grid_point[0] * self.row_size * self.world_to_screen_y

    def drawMap(self, grid):
        """
        Draws initial map with a 50% neutral probability colour

        :type self: object
        :param grid: A list of values that correspond with coordinates
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                idx = row * self.num_cols + column
                temp = [grid[idx]["screen_point_x"], grid[idx]["screen_point_y"]]
                self.occmap_canvas.create_rectangle(temp[0],
                                                    temp[1],
                                                    temp[0]+self.col_offset,
                                                    temp[1]+self.row_offset,
                                                    fill="grey",
                                                    outline="grey")

    def updateMap(self, cells_that_changed, occ_map):
        """
        Take a list of changed cells and updates their colour on the map.

        list -> null
        """

        for cell_to_update in cells_that_changed:
            self.occmap_canvas.create_rectangle(occ_map[cell_to_update]["screen_point_x"],
                                                occ_map[cell_to_update]["screen_point_y"],
                                                occ_map[cell_to_update]["screen_point_x"]+self.col_offset,
                                                occ_map[cell_to_update]["screen_point_y"]+self.row_offset,
                                                fill=occ_map[cell_to_update]["colour"],
                                                outline=occ_map[cell_to_update]["colour"])

    def bindButtons(self, robot_class, window_class, sim_map_class, occ_map):
        """

        """
        window_class.top.bind('<Key-Escape>', lambda event: window_class.close_window())
        
        # Movement
        window_class.top.bind('<Up>', lambda event: command.move(window_class, robot_class, 'Forward'))
        window_class.top.bind('<Down>', lambda event: command.move(window_class, robot_class, 'Reverse'))
        window_class.top.bind('<Left>', lambda event: command.move(window_class, robot_class, 'Turn Left'))
        window_class.top.bind('<Right>', lambda event: command.move(window_class, robot_class, 'Turn Right'))

        # Sensing 
        window_class.top.bind('<s>', lambda event: command.scan_and_update(robot_class,
                                                                                window_class,
                                                                                sim_map_class,
                                                                                occ_map))

        # Movement modifiers
        window_class.top.bind('-', lambda event: command.change_move_step(robot_class, -1))
        window_class.top.bind('+', lambda event: command.change_move_step(robot_class, 1))
        window_class.top.bind('0', lambda event: command.change_move_step(robot_class, 0))
        window_class.top.bind('<Next>', lambda event: command.change_move_step(robot_class, -10))
        window_class.top.bind('<Prior>', lambda event: command.change_move_step(robot_class, +10))

        # UI Modifiers
        window_class.top.bind('r', lambda event: window_class.toggle_overlay())

        # Debugging and testing utilities
        window_class.top.bind('p', lambda event: command.place_obstacle(event, 0, 0, window_class, occ_map))
        window_class.top.bind('l', lambda event: command.place_obstacle(event, 1, 0, window_class, occ_map))
        window_class.top.bind('<Button-2>', lambda event: command.place_obstacle(event, 1, 1, window_class))

        window_class.top.bind('<Return>', lambda event: window_class.start_iterations())
        window_class.top.bind('<space>', lambda event: window_class.toggle_pause())
        window_class.top.bind('<Button-1>', lambda event: window_class.mousePressed(event))
        window_class.top.bind('<B1-Motion>', lambda event: window_class.mouseDragged(event))
        window_class.top.bind('<ButtonRelease-1>', lambda event: window_class.mouseReleased(event))

        # Probability tests        
        window_class.top.bind('o', lambda event: window_class.check_prob(event))
        window_class.top.bind('c', lambda event: window_class.check_prob(event, 1))

        self.initializing = True

    def drawRobot(self, robot_location,
                  robot_body_width,
                  robot_body_length,
                  robot_wheel_length,
                  robot_wheel_width):
        """
        Draws the robot at the location given with scale given in __init__

        :param robot_body_width:
        :param robot_body_length:
        :param robot_wheel_length:
        :param robot_wheel_width:
        :param colour:
        :param wheel_colour:
        :param robot_location: (x, y, theta) in screen coordinates, and degrees
        """
        # TODO: Make this more readable
        robot_x, robot_y, robot_theta = robot_location

        # These are all in world coords
        x = robot_x
        y = robot_y
        orientation = robot_theta
        length = robot_body_length
        width = robot_body_width
        wheel_length = robot_wheel_length
        wheel_width = robot_wheel_width

        canvas = self.occmap_canvas

        steering = 0.0

        # get four points of a car directing east
        # (x,y position is position in the center of the robot)
        corners = [(x - length / 2, y + width / 2),  # back left
                   (x - length / 2, y - width / 2),  # back right
                   (x + length / 2, y - width / 2),  # front right
                   (x + length / 2, y + width / 2)]  # front left
        wheel_centers = [(x - length / 2, y + width / 2),  # back left
                         (x - length / 2, y - width / 2),  # back right
                         (x + length / 2, y)]          # Center front wheel
        wheels = []
        for i in range(len(wheel_centers)):
            xc = wheel_centers[i][0]
            yc = wheel_centers[i][1]
            wheel_corners = [(xc - wheel_length / 2, yc + wheel_width / 2),  # back left
                             (xc - wheel_length / 2, yc - wheel_width / 2),  # back right
                             (xc + wheel_length / 2, yc - wheel_width / 2),  # front left
                             (xc + wheel_length / 2, yc + wheel_width / 2)]  # front left
            wheels.append(wheel_corners)

        n = len(corners)
        for i in range(n):
            corners[i] = self.worldToScreen(corners[i])

        # Draw robot
        canvas.create_oval(corners[0][0], corners[0][1],
                           corners[2][0], corners[2][1],
                           outline=self.robot_colour, fill="", tags="R2")

        number_of_wheels = len(wheels)  # number of wheels
        number_of_corners = len(wheels[0])  # number of corners
        for wheel_idx in range(number_of_wheels):
            corners = wheels[wheel_idx]
            if wheel_idx >= number_of_wheels - 1:
                wheel_x = wheel_centers[wheel_idx][0]
                wheel_y = wheel_centers[wheel_idx][1]
                for corner in range(number_of_corners):
                    corners[corner] = Utils2D.rotate(corners[corner], (wheel_x, wheel_y), steering)
            for i in range(n):
                corners[i] = self.worldToScreen(Utils2D.rotate(corners[i], (x, y), orientation))
            canvas.create_polygon(corners[0][0], corners[0][1],
                                  corners[1][0], corners[1][1],
                                  corners[2][0], corners[2][1],
                                  corners[3][0], corners[3][1],
                                  fill=self.wheel_colour, tags="R2")

    def drawLaser(self, distance):
        """
        Takes the distance data and plots it into a histogram.

        """
        reading_width = int(self.laser_window_width / 360.0)
        reading_height = self.laser_window_height

        # The height of the reading is calculated by getting the percentage of measurement/6000 * reading_height
        # The top part of the rectangle is found by
        # Two ways: paint everything in the canvas red and use the values to mark the rest white.
        # Or, leave white and paint it red.

        for i in range(360):
            self.laserreadout_canvas.create_rectangle(i * self.window_width / 360.0,
                                             150, i * self.window_width / 360.0 + self.window_width / 360.0,
                                             150 - (distance[i] / 40),
                                             fill="red",
                                             tag="Laser")

    def close_window(self):
        self.top.destroy()


if __name__ == '__main__':
    test = Window((800, 600), "Test Window from UI.py")
    test.top.mainloop()