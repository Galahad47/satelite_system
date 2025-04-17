import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2

class ISSInterferenceCalculator:
    def __init__(self):
        self.iss_position = None
        self.receiver_coords = (73.5064, 80.2056)
        self.frequency_band = 'C'
        self.antenna_diameter = None
        self.year = None
        
    def get_iss_position(self):
        try:
            response = requests.get('http://api.open-notify.org/iss-now.json')
            data = response.json()
            self.iss_position = (
                float(data['iss_position']['latitude']),
                float(data['iss_position']['longitude'])
            )
            return self.iss_position
        except Exception as e:
            print(f"Ошибка получения данных МКС: {e}")
            return None

    def set_parameters(self, antenna_diameter, year):
        self.antenna_diameter = antenna_diameter
        self.year = year
        
    def calculate_elevation_angle(self):
        lat1, lon1 = map(radians, self.receiver_coords)
        lat2, lon2 = map(radians, self.iss_position)
        
        dlon = lon2 - lon1
        x = cos(lat2) * cos(dlon)
        y = cos(lat2) * sin(dlon)
        elevation = np.arctan2(np.sqrt(x**2 + y**2), sin(lat2))
        elevation = np.degrees(elevation)
        return elevation

    def calculate_interference_time(self):
        start_date = datetime(self.year, 1, 1)
        end_date = datetime(self.year, 12, 31)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='ME')
        
        results = []
        for date in dates:
            elevation = self.calculate_elevation_angle()
            duration = self.calculate_duration(elevation)
            
            if duration > 0:
                start_time = date.replace(hour=1)
                end_time = start_time + timedelta(hours=duration)
                
                results.append({
                    'date': date.date(),
                    'start_time': start_time.time(),
                    'end_time': end_time.time(),
                    'duration': duration
                })
                
        return pd.DataFrame(results)

    def calculate_duration(self, elevation):
        factor = 1.2
        min_elevation = 5
        
        if elevation < min_elevation:
            return 0
        
        duration = (elevation - min_elevation) / self.antenna_diameter * factor
        return max(duration, 0)

calculator = ISSInterferenceCalculator()

iss_position = calculator.get_iss_position()
if not iss_position:
    print("Не удалось получить данные МКС")

antenna_diameter = float(input("Введите диаметр антенны в метрах: "))
year = int(input("Введите год: "))

calculator.set_parameters(antenna_diameter, year)
result = calculator.calculate_interference_time()


# path = input('/project_D')
data = open('project_D','w+')
data.write(str(result))
data.close()
print(f"Расписание интерференции: \n {result}")