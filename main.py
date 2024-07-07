import pandas as pd
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Sample data
data = {
    'id': [1, 2, 3, 4],
    'event': ['SOSP', 'EOSP', 'SOSP', 'EOSP'],
    'dateStamp': [43831, 43831, 43832, 43832],
    'timeStamp': [0.708333, 0.791667, 0.333333, 0.583333],
    'voyage_From': ['Port A', 'Port A', 'Port B', 'Port B'],
    'lat': [34.0522, 34.0522, 36.7783, 36.7783],
    'lon': [-118.2437, -118.2437, -119.4179, -119.4179],
    'imo_num': ['9434761', '9434761', '9434761', '9434761'],
    'voyage_Id': ['6', '6', '6', '6'],
    'allocatedVoyageId': [None, None, None, None]
}

# Create DataFrame
df = pd.DataFrame(data)

# Convert dateStamp and timeStamp to datetime
df['utc_datetime'] = pd.to_datetime('1900-01-01') + pd.to_timedelta(df['dateStamp'], unit='d') + pd.to_timedelta(df['timeStamp'], unit='d')

# Calculate next event details
df['next_event'] = df['event'].shift(-1)
df['next_utc_datetime'] = df['utc_datetime'].shift(-1)
df['next_lat'] = df['lat'].shift(-1)
df['next_lon'] = df['lon'].shift(-1)

# Calculate durations and distances
df['duration_hours'] = (df['next_utc_datetime'] - df['utc_datetime']).dt.total_seconds() / 3600.0
df['distance_nautical_miles'] = df.apply(lambda row: geodesic((row['lat'], row['lon']), (row['next_lat'], row['next_lon'])).nautical if pd.notnull(row['next_lat']) else np.nan, axis=1)

# Filter for SOSP events
df_sosp = df[(df['event'] == 'SOSP') & (df['next_event'] == 'EOSP')]

# Plot the voyage timeline
plt.figure(figsize=(10, 5))
plt.plot(df_sosp['utc_datetime'], df_sosp['duration_hours'], marker='o', linestyle='-', label='Sailing Time (hours)')
plt.plot(df_sosp['utc_datetime'], df_sosp['distance_nautical_miles'], marker='x', linestyle='--', label='Distance (nautical miles)')
plt.xlabel('UTC Datetime')
plt.ylabel('Value')
plt.title('Voyage Timeline')
plt.legend()
plt.grid(True)
plt.show()
