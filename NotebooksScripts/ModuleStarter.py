#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2024 University of Oxford. All Rights Reserved.
The authors, being Dr Scot Wheeler, have asserted their moral rights.

This is the module docstring. It can be used to introduce the purpose and
key functionality of the module. It will appear in documentation/help.
As an example, in the spyder help window (top right subwindow be default), 
type scipy.optimize to see an example of the docstring for the 
optimize module of the scipy library.

The very first line of the script is an optional shebang line. It tells the 
operating system which interpreter to use to execute the code if the script 
was treated as a stadalone executable.
"""

# Complete the script by filling in the missing code sections marked with <---.

# import required libraries
import math
import numpy as np
import pandas as pd

# =============================================================================
# Calculate PV array size function
# =============================================================================

def calc_pv_array_size(b_length, b_width, panel_w, panel_h, panel_power, roof_angle = 22): # <--- include parameters for building length, width, roof angle, panel width, panel height and panel power
    """
    Calculate the total PV capacity that can be installed on a building's roof

    Parameters
    ----------
    building_width : float
        Width of building in metres.
    building_length : float
        Length of building in metres.
    roof_angle : float
        Angle of the roof from horizontal in degrees.
    pv_width : float
        Width of single PV panel in mm.
    pv_height : float
        Width of single PV panel in mm.
    pv_power : float
        Power of single PV panel in W.

    Returns
    -------
    total_power : float
        Total power of PV array in kW.
    total_panels : float
        Maximum number of PV panels that fit on the roof.
    
    """
    # Convert to meters 
    panel_h = panel_h*1e-3
    panel_w = panel_w*1e-3

    # Assuming we place the panels in horizontal orientaion
    true_building_width = b_width/math.cos(math.radians(roof_angle))
    panels_along_length = b_length//(panel_h) # Number of panels along length
    panels_along_width = true_building_width//(panel_w) 
    total_panels = panels_along_length * panels_along_width
    return panel_power*total_panels, total_panels

# =============================================================================
# Example PV class
# =============================================================================
class PV():
    """
    PV object

    Parameters
    ----------
    pv_id : str
        Unique identifier for the PV asset.
    capacity_factor : list or numpy array
        Capacity factor (kW/kWp) profile for the PV asset.
    dt : float
        Time step in hours.
    peak_power_kw : float, optional
        Peak power of the PV asset in kW. The default is 4.0 kW.
    """

    def __init__(self, pv_id, capacity_factor, dt, peak_power_kw=4.0,):
        self.id = pv_id
        self.capacity_factor = capacity_factor
        self.peak_power_kw = peak_power_kw
        self.T = len(capacity_factor)
        self.dt = dt

        # we can call the method to calculate the output profile on initialisation
        self.pv_output = self.pv_power_output()

    def pv_power_output(self):
        """
        Calculate the PV power output profile.

        Returns
        -------
        pv_output : list
            Power output profile of the PV asset in kW.
        """
        self.pv_output_p = self.capacity_factor * self.peak_power_kw
        return self.pv_output_p

# =============================================================================
# Basic conditional battery class
# =============================================================================
class Storage():
    """
    Storage object

    Parameters
    ----------
    id : str
        Unique identifier for the battery asset.
    T : int
        Total number of time periods.
    max_soc : float, optional
        Maximum state of charge (kWh). The default is 10.0 kWh.
    min_soc : float, optional
        Minimum state of charge (kWh). The default is 1.0 kWh.
    max_power : float, optional
        Maximum power the battery can handle (kW). The default is 15.0 kW.
    efficiency : float, optional
        Base battery efficiency. The default is 0.98.
    dt_degradation : float, optional
        Battery degradation factor. The default is 0.01.
    soc_0 : float, optional
        Initial state of charge (kWh). The default is 5.0 kWh.
    model : str, optional
        Battery model name. The default is "Tesla Powerwall".
    """

    def __init__(self, id, T, dt, max_soc=10.0, min_soc=1.0, max_power=15.0,
                  efficiency=0.98, dt_degradation=0.01, soc_0=5.0,
                    model="Tesla Powerwall"):
        self.id = id
        self.T = T # Total number of time periods
        self.dt = dt # Time step in hours
        self.max_soc = max_soc  # Maximum state of charge (kWh)
        self.min_soc = min_soc   # Minimum state of charge (kWh)
        self.max_power = max_power # Maximum power the battery can handle (kW)
        self.efficiency = efficiency    # Base battery efficiency
        self.dt_degradation = dt_degradation    # Battery degradation factor
        self.soc_0 = soc_0  # Initial state of charge (kWh)
        self.model = model  # Battery model name

        self.storage_power = [0] * self.T  # Initialize storage power list
        self.soc_E = [self.soc_0] * self.T  # Initialize state of charge list
        

    def battery_charge_action(self, demand_P, t):
        """
        This function decides if to charge or discharge a battery based on a 
        simple conditional battery model, within a single time period t of length dt.
        It returns the net demand after the storage action.
        
        Parameters
        ----------
        demand_P : float
            The power demand (units of power e.g. kW)
        t : int
            The current time period index.
            
        Returns
        -------
        net_demand : float
            The net demand post battery operation.
        """
        # add you conditional battery model from above, adjusting to include
        # the self keyword.
        if demand_P > 0:  
            # <--- add your code to discharge the battery (remember the first period, t=0, is dealt with separately)
            if t == 0:
                self.storage_power[t] = -1* min(self.max_power, self.soc_0 - self.min_soc, demand_P)
            else:
                # Also check how much power is left to give
                self.storage_power[t] = -1*min(self.max_power, (self.soc_E[t-1]- self.min_soc)*self.efficiency/self.dt, demand_P)
        
        elif demand_P < 0:  
            if t == 0:
                self.storage_power[t] = min(self.max_power, (self.max_power - self.soc_0), -1*demand_P)
            else:
                # Compare with how much space is available to ingest the power
                self.storage_power[t] = min(self.max_power, (self.max_soc-self.soc_E[t-1])*self.efficiency/self.dt, -1*demand_P)

        else:
            self.storage_power[t] = 0
            
        # update the state of charge
        if t == 0:
            self.soc_E[0] = self.soc_0 + self.storage_power[t]*self.dt  # Maintain initial SoC
        else:
            self.soc_E[t] = self.soc_E[t-1] + self.storage_power[t]*self.dt
        

        # and calculate net_power
        net_demand = demand_P + self.storage_power[t]
        
        return net_demand


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
    
    
    
    pass