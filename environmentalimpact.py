# CO2 impact based on the Netherlands (kg CO2e per unit)

co2_impact = {
    "beef": 60,  # per kg
    "lamb/mutton": 24,  # per kg
    "cheese": 21,  # per kg
    "chocolate": 19,  # per kg
    "coffee": 17,  # per kg
    "prawns": 12,  # per kg
    "pig meat": 7,  # per kg
    "poultry meat": 6,  # per kg
    "fish farmed": 5,  # per kg
    "milk": 3,  # per litre
    "gasoline": 3.14,  # per litre
    "electricity": 0.27,  # per kWh
    "rice": 4,
    "eggs": 0.3,  # per egg
    "air travel": 0.15,  # per km per passenger
    "train travel": 0.05,  # per km per passenger
    "natural gas": 1.78,  # per m3
    "beer": 0.7,  # per litre
    "wine": 1.5,  # per litre
    "smartphone": 70,  # per device (production)
    "clothing": 15,  # per pair (production)
    "bus travel": 0.09,  # per km per passenger
}

# --- Input variables ---
# Food (kg per week)
beef_per_week = 0.6
lamb_per_week = 0
cheese_per_week = 0
chocolate_per_week = 0
coffee_per_week = 0.1
prawns_per_week = 0
pig_meat_per_week = 0.2
poultry_meat_per_week = 0.5
fish_farmed_per_week = 0
milk_per_week = 0  # litres
rice_per_week = 0.1
eggs_per_week = 6

# Drinks (litres per week)
beer_per_week = 0
wine_per_week = 0

# Transport
gasoline_km_per_year = 6000
gasoline_efficiency_l_per_100km = 6.5
air_travel_km_per_year = 7000
train_km_per_year = 1000
bus_km_per_year = 100

# Home energy
electricity_kwh_per_year = 2800
natural_gas_m3_per_year = 670

# Consumer goods
smartphones_per_year = 0.5
clothing_items_per_year = 10

# --- Calculation ---
weeks_per_year = 52

category_emissions = {
    "beef": beef_per_week * weeks_per_year * co2_impact["beef"],
    "lamb/mutton": lamb_per_week * weeks_per_year * co2_impact["lamb/mutton"],
    "cheese": cheese_per_week * weeks_per_year * co2_impact["cheese"],
    "chocolate": chocolate_per_week * weeks_per_year * co2_impact["chocolate"],
    "coffee": coffee_per_week * weeks_per_year * co2_impact["coffee"],
    "prawns": prawns_per_week * weeks_per_year * co2_impact["prawns"],
    "pig meat": pig_meat_per_week * weeks_per_year * co2_impact["pig meat"],
    "poultry meat": poultry_meat_per_week * weeks_per_year * co2_impact["poultry meat"],
    "fish farmed": fish_farmed_per_week * weeks_per_year * co2_impact["fish farmed"],
    "milk": milk_per_week * weeks_per_year * co2_impact["milk"],
    "rice": rice_per_week * weeks_per_year * co2_impact["rice"],
    "eggs": eggs_per_week * weeks_per_year * co2_impact["eggs"],
    "beer": beer_per_week * weeks_per_year * co2_impact["beer"],
    "wine": wine_per_week * weeks_per_year * co2_impact["wine"],
    "gasoline": (gasoline_km_per_year / 100)
    * gasoline_efficiency_l_per_100km
    * co2_impact["gasoline"],
    "air travel": air_travel_km_per_year * co2_impact["air travel"],
    "train travel": train_km_per_year * co2_impact["train travel"],
    "bus travel": bus_km_per_year * co2_impact["bus travel"],
    "electricity": electricity_kwh_per_year * co2_impact["electricity"],
    "natural gas": natural_gas_m3_per_year * co2_impact["natural gas"],
    "smartphone": smartphones_per_year * co2_impact["smartphone"],
    "clothing": clothing_items_per_year * co2_impact["clothing"],
}

total_emissions = sum(category_emissions.values())

# Calculate percentages and sort
percentages = {
    k: (v / total_emissions * 100 if total_emissions > 0 else 0)
    for k, v in category_emissions.items()
}
sorted_categories = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

# --- Output ---
print(f"Total annual CO2 emissions: {total_emissions:.2f} kg")
print("Breakdown by category (highest to lowest):")
for cat, perc in sorted_categories:
    print(f"{cat}: {category_emissions[cat]:.1f} kg ({perc:.1f}%)")
