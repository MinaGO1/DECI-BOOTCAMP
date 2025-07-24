import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

n_rows = 1000
mean_closure_per_opening = 18
std_closure_per_opening = 5
mean_vehicle_flow_hr = 3250
std_vehicle_flow_hr = 400

base_date = datetime(2025, 5, 1)

data = []

bridge_names = ["El Ferdan", "Martyr-El-Sayed", "Martyr-Abul-Makarem", "Ahmed-el-Mansy", "Taha-Zaki-Abdullah"]
bridge_types = {
    "El Ferdan": "Swing",
    "Martyr-El-Sayed": "Floating",
    "Martyr-Abul-Makarem": "Floating",
    "Ahmed-el-Mansy": "Pontoon",
    "Taha-Zaki-Abdullah": "Pontoon"
}
base_mean_ships = {
    "Swing": 2.5,
    "Floating": 1.3,
    "Pontoon": 0.9
}

for i in range(n_rows):
    date = base_date + timedelta(days=i)
    random_time = timedelta(hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
    current_datetime = date + random_time
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M")

    bridge_name = np.random.choice(bridge_names)
    bridge_type = bridge_types[bridge_name]

    # Ship traffic with more noise
    mean_openings = base_mean_ships[bridge_type] + np.random.normal(0, 0.6)
    ships_per_day = np.random.poisson(max(mean_openings, 0.3))
    ship_present = "YES" if ships_per_day > 0 else "NO"

    closure_durations = np.random.normal(mean_closure_per_opening, std_closure_per_opening + np.random.rand(), ships_per_day)
    closure_min = max(0, round(np.sum(closure_durations))) if ships_per_day > 0 else 0

    # Heavier-tailed variation (simulate occasional spikes)
    vehicle_flow = int(np.random.normal(mean_vehicle_flow_hr, std_vehicle_flow_hr + 100 * np.random.rand()))
    vehicle_flow += int(np.random.choice([0, -200, 200, -150, 150, 0, 0], p=[0.05, 0.05, 0.05, 0.05, 0.05, 0.35, 0.4]))
    vehicle_flow = max(800, min(vehicle_flow, 6000))

    if closure_min > 0 and vehicle_flow > 0:
        affected_vehicles = vehicle_flow * (closure_min / 60)
        delay_min_per_vehicle = closure_min / (affected_vehicles + np.random.uniform(0.2, 2.5))
        delay_min_per_vehicle += np.random.normal(0, 0.03)
        delay_min_per_vehicle = max(0, round(delay_min_per_vehicle, 3))
    else:
        delay_min_per_vehicle = 0.0

    hour = current_datetime.hour
    is_rush = hour in [7, 8, 17, 18]

    # Add noise to rush hour logic
    rush_hour = "YES" if is_rush and np.random.rand() > 0.25 else "NO"

    # Fuzzy period_of_day assignment
    if 5 <= hour < 12:
        period_of_day = np.random.choice(["Morning", "Daytime", "Rush Hour"], p=[0.6, 0.3, 0.1])
    elif 12 <= hour < 17:
        period_of_day = np.random.choice(["Afternoon", "Daytime"], p=[0.7, 0.3])
    elif 17 <= hour < 21:
        period_of_day = np.random.choice(["Evening", "Rush Hour", "Afternoon"], p=[0.6, 0.25, 0.15])
    else:
        period_of_day = np.random.choice(["Night", "Late Night"], p=[0.7, 0.3])

    data.append({
        "DateTime": datetime_str,
        "Bridge_Type": bridge_type,
        "Bridge_Name": bridge_name,
        "Ships_per_day": ships_per_day,
        "ship_present": ship_present,
        "Closure_min": closure_min,
        "vehicle_flow_veh_hr": vehicle_flow,
        "delay_min_per_vehicle": delay_min_per_vehicle,
        "period_of_day": period_of_day,
        "rush_hour": rush_hour,
    })

df_noisy_sim = pd.DataFrame(data)
df_noisy_sim.to_csv("Traffic_noisy.csv", index=False)

print(df_noisy_sim.head())
print("\nColumns:", df_noisy_sim.columns.tolist())
