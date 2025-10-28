"""
Battery Modeling Tutorial - Loops and Conditionals
This file demonstrates Python loops and conditional statements through 
a practical battery charging/discharging simulation over 10 time periods.

Learning objectives:
- Using for loops 
- Working with conditional statements (if/elif/else)
- List indexing and manipulation
- Variable assignment and updates

Complete the script by filling in the missing code sections marked with <---.

1) Initially, ignore any battery constraints e.g. max/min state of charge, max power, efficiency, degradation etc
2) Revisit your completed code from (1) and add battery constraints. 
    You could do this by adding more nested if statements, or using min/max functions when calculating battery power.
3) finally, consider how you would model battery efficiency and degradation over time.

This is a comment block or docstring which can span multiple lines. 
It is often used at the start of files to describe the file.
@author: Wilhem Hector
"""

# import math

# Initialize battery parameters and variables
dt = 1  # Time step in hours
max_soc = 10  # Maximum state of charge (kWh)
min_soc = 1   # Minimum state of charge (kWh)
max_power = 15 # Maximum power the battery can handle (kW)
efficiency = 0.98    # Base battery efficiency
dt_degradation = 0.01    # Battery degradation factor
soc_0 = 5  # Initial state of charge (kWh)

# Create the demand variable as a list (this represents energy demand over 10 periods)
# Positive values indicate demand is needed from the battery
# Negative values indicate excess energy that can be used to charge the battery
demand_P = [5, -8, 12, -3, 7, -10, 15, -5, 8, -2]


# Initialize lists to store battery power, state of charge and the new net demand after battery operation
bat_P = [0] * len(demand_P)  # List to store battery power for each period, initialized to 0
soc_E =  [soc_0] * len(demand_P) # <--- List to store state of charge, starting at 5 kWh
net_demand_P = [0] * len(demand_P) # <--- List to store net demand after battery operation

# iterate through each time period using the range() function
for t, _ in enumerate(demand_P): # <--- Fill in the for loop to iterate over the range of demand_P length
    
    # Conditional logic - check if demand is positive, negative or 0
    if demand_P[t]> 0: # <--- Complete the condition to check if demand is positive
        # Case (a): Positive demand means discharge the battery
        # Calculate battery power considering efficiency and available SOC
        max_dischage_power = min(max_power, (soc_E[t-1]- min_soc)*efficiency/dt)
        bat_P[t] = -1*min(max_dischage_power, demand_P[t])
        
    elif demand_P[t] < 0: # <--- complete the else if condition to check if demand is negative:
        # Case (b): Negative demand means charge the battery  
        bat_P[t] = min(-1*demand_P[t], max_power, (max_soc-soc_E[t-1])/efficiency*dt)

    else:
        # Case (c): Zero demand means no battery operation
        bat_P[t] = 0  # No power change

    # Update state of charge (SoC) based on battery power and time step
    if t == 0:
        soc_E[0] = soc_0 + bat_P[t]*dt  # Maintain initial SoC
    else:
        soc_E[t] = soc_E[t-1] + bat_P[t]*dt # Update SoC based on previous timestep's SoC and battery power, remember you need to convert power to energy

    # update the net demand after battery operation
    net_demand_P[t] = demand_P[t] + bat_P[t]

# Print the final state of charge
print(f'The final state of charge is: {soc_E[-1]} kwh') # <--- Add a print statement to display the final state of charge. 
print(f'The net demand: {net_demand_P}')

