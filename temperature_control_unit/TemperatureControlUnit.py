if __name__ == "__main__":
    import sys
    import os
    # Add the parent directory of the current script to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from states_enum.States import States_SCU, States_TCU
import time
import threading


class TemperatureControlUnit:
    def __init__(self, event_system=None):
        # Start coffee machine with heater off
        self.state = States_TCU.OFF
        self.event_system = event_system
        if event_system is not None:
            self.event_system.subscribe(self)
            
        # Water properties
        self.temp_ambient = 23
        self.temp = self.temp_ambient
        self.temp_desired = 40
        self.temp_lock = threading.Lock()
        
        # Heater properties
        self.Cdegrees_increase_per_loop = 2
        self.heater_loop_time = 0.05
        # Sensor properties
        self.sensor_polling_rate = 0.03
        self.threads_timeout = 10
        # sensor polling having a higher rate than heat adding means it can/will overshoot
         
    def get_state(self):
        return self.state
    
    def set_state(self, tcu_state):
        self.state = tcu_state
        return self.state
    
    def set_and_pub_self_signed_event(self, event):
        self.set_state(event)
        if self.event_system is not None:
            self.event_system.publish_event(event, self)
    
    def event_handler(self, event):

        if event == States_SCU.OFF:
            self.set_state(States_TCU.OFF)

        elif isinstance(event, list):
            if event[0] == States_SCU.VALID_REQUEST:
                self.temp_desired = event[1]
                self.set_state(States_TCU.HEATING)
                self.start_brewing()
                
        elif event == States_SCU.WAITING:
            self.set_state(States_TCU.OFF)   
               
    def start_brewing(self):
        """Starts heating procedure setup
            sets and publishes States_TCU.READY flag
        """
        
        if self.get_state() == States_TCU.HEATING:
            
            # Start Double Thread
            heating_thread = threading.Thread(target=self.start_heating)
            sensor_thread = threading.Thread(target=self.reach_desired_temperature)
            
            sensor_thread.start()
            heating_thread.start()

            sensor_thread.join(self.threads_timeout)
            heating_thread.join(self.threads_timeout)
     
            if heating_thread.is_alive():        
                print("\n Thread Timeout, Stopped heating water somethings wrong")
                self.set_state(States_TCU.OFF)
            else:    
                self.set_and_pub_self_signed_event(States_TCU.READY)
        else:
            print("ERROR: to start brewing tcu needs to be in HEATING STATE")
            
    def start_heating(self):
        # Simulate the heating process (Turned on the heater, waiting for signal from sensor to turn off)
        time.sleep(self.heater_loop_time)
        while self.get_state() == States_TCU.HEATING:
            with self.temp_lock:
                self.temp += self.Cdegrees_increase_per_loop
            time.sleep(self.heater_loop_time)
                # In a real embedded system, this might involve interacting with hardware
        
    def reach_desired_temperature(self):
        # Simulate reaching the desired temperature (Simulating polling the sensor for temperature readings)
        while self.get_state() == States_TCU.HEATING:
            with self.temp_lock:
                if self.temp >= self.temp_desired:
                # In a real embedded system, this might involve temperature sensors
                    self.set_state(States_TCU.READY)  # Both threads should end before publishing state 
            time.sleep(self.sensor_polling_rate)


def temp_decay(tcu: TemperatureControlUnit):
    """
    Simulates the temperature decay of water when tcu is in state OFF
    """
    water_temp_after_decay = 0.9  # 90%

    while True:
        if tcu.get_state() == States_TCU.OFF:
            if tcu.temp > tcu.temp_ambient:
                tcu.temp *= water_temp_after_decay
            else:
                tcu.temp = tcu.temp_ambient
            time.sleep(1)                


if __name__ == "__main__":
    tcu = TemperatureControlUnit()
    tcu.state = "HEATING"
    start = time.time()
    tcu.event_handler([States_SCU.VALID_REQUEST, 9090])
  
    print(f"Took {time.time() - start:0.2f} s to heat\
 water from {tcu.temp_ambient} to {tcu.temp} at\
 rate {tcu.Cdegrees_increase_per_loop} \
 C every {tcu.heater_loop_time}\
 s \n")
    print(f"sensor rate: {tcu.sensor_polling_rate}")
    print(tcu.state)
    
    