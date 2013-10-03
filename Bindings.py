#!/usr/bin/env python
__author__ = 'Theo'
__copyright__ = "Copyright 2013, theo.is-a-geek.com"
__credits__ = ["Theo Deyle"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Theo Deyle"
__email__ = "theo.deyle@gmail.com"
__status__ = "Hashing Out"

# Bindings for all of the buttons
def bindAllButtons(robot, sim_window):
    """
    Binds all of the buttons
    """
    sim_window.top.bind('<Key-Escape>', lambda event: sim_window.close_windows(sim_window))
