import math

# Constants for the saturation vapor pressure calculation
T = -70  # temperature in Celsius
T_kelvin = T + 273.15  # convert to Kelvin

# The saturation vapor pressure formula
# Using the formula for ice (since -70C is well below freezing)
# This is a simplified version of the formula, accurate at very low temperatures
E_ice = 6.11 * 10 ** ((9.5 * T) / (265.5 + T))

# Convert vapor pressure from millibars to pascals
E_ice_pascals = E_ice * 100

# Density of water vapor (ideal gas law): ρ = P / (R * T)
# Where P is the vapor pressure, R is the specific gas constant for water vapor, and T is the temperature in Kelvin
R = 461.5  # specific gas constant for water vapor in J/(kg·K)
density_water_vapor = E_ice_pascals / (R * T_kelvin)  # in kg/m³

# Convert kg/m³ to g/m³
density_water_vapor_g_m3 = density_water_vapor * 1000  # in g/m³

density_water_vapor_g_m3

