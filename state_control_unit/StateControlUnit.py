import time
import threading
from enum import Enum

class States_TCU(Enum):
    OFF="OFF"
    HEATING = "HEATING" 
    READY = "READY"

class States_SCU(Enum):
    OFF="OFF"
    WAITING = "WAITING"
    VALID_REQUEST = "VALID_REQUEST"

class TemperatureControlUnit:
    def __init__(self):
        # Start coffee machine with heater off
        self.state = States_TCU.OFF
        # Water properties
        self.temp_ambient = 23
        self.temp         = self.temp_ambient
        self.temp_desired = 80
        self.temp_lock = threading.Lock()
        # Heater properties
        self.Cdegrees_increase_per_loop = 4
        self.heater_loop_time = 0.1
        # Sensor properties
        self.sensor_polling_rate = 0.3
        # sensor polling having a diff rate than heat adding means it can/will overshoot
    
    def get_state(self):
        return self.state
    
    def set_state(self, tcu_state):
        self.state = tcu_state
        return self.state
    
    def start_brewing(self):
        """Starts heating procedure setup
        """        
        self.set_state(States_TCU.HEATING)
        #Start Double Thread
        heating_thread = threading.Thread(target=self.start_heating)
        sensor_thread = threading.Thread(target=self.reach_desired_temperature)
        
        sensor_thread.start()
        heating_thread.start()
        
        sensor_thread.join()
        heating_thread.join()
        

    def start_heating(self):
        # Simulate the heating process (Turned on the heater, waiting for signal from sensor to turn off)
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
                    self.set_state(States_TCU.READY)  # mimicks trigger response from sensor
            time.sleep(self.sensor_polling_rate)


class StateControlUnit(): # CoffeeMachine
    def __init__(self):
        # how can i decouple the tcu from scu, I should publish the state and the
        self.tcu = TemperatureControlUnit() 
        self.state = States_SCU.OFF 
        
        self.available_coffees = "5"
        self.escape_menu_key = "q"
        self.valid_request = False
        
        self.water_temp_decay = False
        self.water_temp_decay_rate = 2
            
    def get_state(self):
        return self.state
    
    def set_state(self, scu_state):
        self.state = scu_state
        return self.state
        
    def turn_on_machine(self):
        """Turns Machine on
            State Transition (SCU): OFF -> WAITING
        """
        if self.get_state() == States_SCU.OFF:     
            print("Starting operations\n")
            self.set_state(States_SCU.WAITING)

    def turn_off_machine(self):
        """Turns Machine off
            State Transition (SCU,TCU): *ANY -> OFF
        """
        print("Turning off TemperatureControlUnit and cancelling any operation\n")
        self.tcu.set_state(States_TCU.OFF)
        self.set_state(States_SCU.OFF) 
        
    def shutdown_button_pressed(self):
        """sends kill signal, runs on a daemon thread"""
        #TODO: BUTTON PRESSED
        self.turn_off_machine() # logic will kill heating threads
        
    def select_coffee_brewing_option(self):
        """ Coffee menu, requests input from user with number associated with coffee
            State Transition (SCU): WAITING -> VALID_REQUEST
        """
        #TODO: change coffee selection criteria (like list with entries [coffee, amount])
        if self.get_state() == States_SCU.WAITING:
            self.valid_request = False
            print(f"\nSelect Coffee: 1-{self.available_coffees}, \
                  {self.escape_menu_key} to quit\n")
            menu_option = input()
            if menu_option == self.escape_menu_key:
                self.turn_off_machine()
            elif int(menu_option) <= int(self.available_coffees): # kinda shitty
                self.valid_request = True
                return self.valid_request
            else:
                print("Invalid coffee selection. Please try again.")
            return self.valid_request
        
    def send_request_to_tcu_brew(self, valid_request):
        """sends brew signal if request is valid else, does nothing""" 
        if valid_request:
            self.tcu.start_brewing()
             
    def serve_coffee(self):
        """Performs Operation. 
            State Transition: READY -> WAITING
        """
        if self.tcu.get_state() == States_TCU.READY:
            print("Coffee served\n")
            
            self.tcu.set_state(States_TCU.OFF)
            self.set_state(States_SCU.WAITING)
                

def temp_decay(coffee_machine: StateControlUnit):
    """
    Simulates the temperature decay of water when heater is in state OFF or WAITING
    """
    while True:
        if coffee_machine.tcu.get_state() == States_TCU.OFF:
            # should be getting and setting temp from functions
            new_temp = coffee_machine.tcu.temp - coffee_machine.water_temp_decay_rate
            if new_temp >= coffee_machine.tcu.temp_ambient:
                coffee_machine.tcu.temp = new_temp
            else:
                coffee_machine.tcu.temp = coffee_machine.tcu.temp_ambient
            time.sleep(1)


if __name__ == '__main__':
    coffee_machine = StateControlUnit()
    
    coffee_machine.turn_on_machine()
    # shutdown_button = threading.Thread(target=coffee_machine.shutdown_button_pressed, daemon=True)
    # shutdown_button.start()
    water_decay_thread = threading.Thread(target=temp_decay, args=(coffee_machine,), daemon=True)
    water_decay_thread.start()
    print(f"Water temp: {coffee_machine.tcu.temp}")
    #TODO: Make it break loop whenever needed
    while coffee_machine.get_state() != States_SCU.OFF:
        request = coffee_machine.select_coffee_brewing_option()
        coffee_machine.send_request_to_tcu_brew(valid_request = request)
        coffee_machine.serve_coffee()
        print(f"Water temp: {coffee_machine.tcu.temp}")
        
    print("finished")
    coffee_machine.turn_off_machine()
    
    