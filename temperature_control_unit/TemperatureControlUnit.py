import time
import threading

class TemperatureControlUnit:
    def __init__(self):
        self.state = "OFF"
        self.temp_ambient = 23
        self.temp         = self.temp_ambient
        self.temp_desired = 80
        self.temp_lock = threading.Lock()
        self.Cdegrees_per_time = 4
    
    def get_state(self):
        return self.state
    
    def set_state(self, tcu_state):
        self.state = tcu_state
        return self.state
    
    def start_heating(self):
        if self.state == "HEATING":
            # Simulate the heating process (Turned on the heater)
            while self.state == "HEATING":
                with self.temp_lock:
                    self.temp += self.Cdegrees_per_time
                time.sleep(0.1)
                    # In a real embedded system, this might involve interacting with hardware
        
    def reach_desired_temperature(self):
        if self.state == "HEATING":
            # Simulate reaching the desired temperature (Simulating polling the sensor for temperature readings)
            while self.state == 'HEATING':
                with self.temp_lock:
                    if self.temp >= self.temp_desired:
                    # In a real embedded system, this might involve temperature sensors
                        self.state = "READY" # mimicks sending a stop command to the heater
                time.sleep(0.3)
                

if __name__ == "__main__":
    tcu = TemperatureControlUnit()
    tcu.state = "HEATING"
    start = time.time()
    heating_thread = threading.Thread(target=tcu.start_heating)
    sensor_thread = threading.Thread(target=tcu.reach_desired_temperature)
    
    heating_thread.start()
    sensor_thread.start()
    
    heating_thread.join()
    sensor_thread.join()
    
    print("Threading Took:" + time.time() - start)
    print(tcu.state)
    
    