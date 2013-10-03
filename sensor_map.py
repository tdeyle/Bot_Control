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
from Tkinter import *

class SensorMap:
    def __init__(self, type, range, resolution, offset, FOV=360, window=[200,200]):
        """ (str, int, int, list[int], int, list[int]) -> list[ints]

        Builds a 200px x 200px map that represents a sensor - sonar, or laser.
        :param type: Type and location of sensor, ex., Left Sonar, Laser
        :param range: Range of Sensor in mm
        :param resolution: Resolution of map in mm
        :param offset: integer list consisting of Offset of Sensor along x, y and angle to robot center.
        :param FOV: default 360 degrees, laser sensor
        :param window: default 200 x 200px
        """
        self.resolution = resolution
        self.width, self.height = range, range
        self.x_offset, self.y_offset, self.ang_offset = offset

        self.top = Tk()
        self.world_width, self.world_height = self.width, self.height
        self.window_width, self.window_height = window

        sensor_map_window = Frame(self.top)
        sensor_map_window.pack()
        self.sensor_map_canvas = Canvas(sensor_map_window,
                                        bg="grey",
                                        height=self.window_height,
                                        width=self.window_width)

        self.sensor_map_canvas.pack(fill=BOTH, expand=1)

        self.top.title(type)
        self.top.mainloop()

    def anothermethod(self):
        """
        Takes the distance_readings and determines whether it an obstacle was found. It marks the information
         a map.
        :param distance_readings:
        :param robot: robot instance to grab the

        :return: None
        """
        pass

    def redraw(self):
        """
        Redraws the map with the settings

        :return: None
        """
        pass

    def reset(self):
        """
        Resets the local sensor map to 0.5 prior probability

        :return: None
        """

if __name__ == '__main__':
    a = SensorMap("Sonar", 5000, 10, [0, 0, 0])
    #b = SensorMap("Sonar", 5000, 10, 80)
    #c = SensorMap("Laser", 6000, 10)
    #print a.width, a.height
    #print b.width, b.height
    #print c.width, c.height
