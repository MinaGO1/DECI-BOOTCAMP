| Column Name             | Description                                                 | Data Type         | Example Value |
| ----------------------- | ----------------------------------------------------------- | ----------------- | ------------- |
| `Date`                  | Date of the record.                                         | Date (YYYY-MM-DD) | `2025-07-01`  |
| `Bridge_Type`           | Type of the bridge: Swing, Floating, or Pontoon.            | String            | `Swing`       |
| `Bridge_Name`           | Name of the specific bridge.                                | String            | `El Ferdan`   |
| `Ships_per_day`         | Number of ships passing per day.                            | Integer           | `37`          |
| `ship_present`          | Indicates if a ship is present (`YES`) or not (`NO`).       | String            | `YES`         |
| `Closure_min`           | Duration in minutes the bridge is closed for ship passage.  | Integer           | `180`         |
| `vehicle_flow_veh_hr`   | Number of vehicles passing per hour during bridge closure.  | Integer           | `6000`        |
| `delay_min_per_vehicle` | Average delay in minutes per vehicle due to bridge closure. | Float             | `3.0`         |
| `traffic_level`         | Categorization of traffic level: Light, Moderate, or Heavy. | String            | `Heavy`       |
