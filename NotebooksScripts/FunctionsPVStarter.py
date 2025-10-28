"""
Functions, Classes and Modules Tutorial
This file demonstrates Python functions.

Learning objectives:
- Defining and using functions

Complete the script by filling in the missing code sections marked with <---.

@author: Wilhem Hector
"""

# Import any necessary libraries
import math
import pandas as pd
import numpy as np
import os

# <--- Define a function to size a PV system based on building dimensions and panel specifications
def calculate_pv_size(b_length, b_width, panel_w, panel_h, panel_power, roof_angle = 22): # <--- include parameters for building length, width, roof angle, panel width, panel height and panel power
    """
    Calculate the total PV capacity that can be installed on a building's roof
    
    """
    # Convert to meters 
    panel_h = panel_h*1e-3
    panel_w = panel_w*1e-3

    # Assuming we place the panels in horizontal orientaion
    true_building_width = b_width/math.cos(math.radians(roof_angle))
    panels_along_length = b_length//(panel_h) # How many along the length
    panels_along_width = true_building_width//(panel_w) 
    total_panels = panels_along_length * panels_along_width
    return panel_power*total_panels, total_panels

if __name__ == "__main__":
    # =============================================================================
    # This section is a common way to incorporate code that you want to run if the 
    # script is executed directly, but will be ignored if the script is 
    # imported as a module into another. 
    # 
    # It separates the executable part of the script from the part that defines
    # reusable components e.g. functions.
    # 
    # This is useful way of testing the code or providing examples of how to 
    # use the code.
    # =============================================================================
    
    pv_capacity_kw, num_panels = calculate_pv_size (30, 8, 1046, 1690, 400 )# <--- call the calculate_pv_size function with appropriate arguments

    print(f'The capacity of the house is {pv_capacity_kw} Wp, with {num_panels} panels') # <--- Add a print statement to display the number of PV panels and the total PV capacity in kW
