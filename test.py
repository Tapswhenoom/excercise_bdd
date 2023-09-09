import time
import threading
from enum import Enum

class EventSystem:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish_event(self, event, publisher = None):
        for subscriber in self.subscribers:
            subscriber.event_handler(event, publisher)


class States_TCU(Enum):
    OFF="OFF"
    HEATING = "HEATING" 
    READY = "READY"


class States_SCU(Enum):
    OFF="OFF"
    WAITING = "WAITING"
    VALID_REQUEST = "VALID_REQUEST"


class TemperatureControlUnit:
    def __init__(self, event_system = None):
        # Start coffee machine with heater off
        self.state = States_TCU.OFF
        self.event_system = event_system
        if event_system != None:
            self.event_system.subscribe(self)
            
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
    
    def set_and_pub_self_signed_event(self, event):
        self.set_state(event)
        if self.event_system is not None:
            self.event_system.publish_event(event, self)
    
    def event_handler(self, event, publisher):
        if publisher is not None and publisher == self:
            return
        if event == States_SCU.OFF:
            self.set_state(States_TCU.OFF)
        elif event == States_SCU.VALID_REQUEST:
            self.start_brewing()
        elif event == States_SCU.WAITING:
            self.set_state(States_TCU.OFF)         
    
    def start_brewing(self):
        """Starts heating procedure setup
            State Transition (TCU): OFF -> (HEATING) -> READY

        """        
        self.set_state(States_TCU.HEATING)
        #Start Double Thread
        heating_thread = threading.Thread(target=self.start_heating)
        sensor_thread = threading.Thread(target=self.reach_desired_temperature)
        
        sensor_thread.start()
        heating_thread.start()
        
        sensor_thread.join()
        heating_thread.join()
        
        # just publishing the state, the state at this point is already READY
        self.set_and_pub_self_signed_event(States_TCU.READY)

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
                    self.set_state(States_TCU.READY)  # Both threads should end before publishing state 
            time.sleep(self.sensor_polling_rate)
        


class StateControlUnit(): # CoffeeMachine
    def __init__(self, event_system = None):
        # how can i decouple the tcu from scu, I should publish the state and the
        #self.tcu = TemperatureControlUnit() 
        self.state = States_SCU.OFF 
        self.event_system = event_system
        if event_system != None:
            self.event_system.subscribe(self)
        
        self.available_coffees = {"1": "Espresso", "2" :"Cappuccino", "3" : "Latte",
                                  "4" : "Americano", "5" : "Iced Coffee", "6" : "Black Coffee"}
        self.escape_menu_key = "q"
        self.menu_option = None
            
    def get_state(self):
        return self.state
    
    def set_state(self, scu_state):
        self.state = scu_state
        return self.state
    
    def set_and_pub_self_signed_event(self, event):
        self.set_state(event)
        if self.event_system is not None:
            self.event_system.publish_event(event, self)
        
    def event_handler(self, event, publisher):
        if publisher is not None and publisher == self:
            return 
        if event == States_TCU.READY:
            self.serve_coffee()
        
    def turn_on_machine(self):
        """Turns Machine on
            State Transition (SCU): OFF -> WAITING
            triggering:
            State Transition (TCU): OFF -> OFF
        """
        if self.get_state() == States_SCU.OFF:     
            print("Starting operations\n")
            self.set_and_pub_self_signed_event(States_SCU.WAITING)

    def turn_off_machine(self):
        """Turns Machine off
            State Transition (SCU,TCU): *ANY -> OFF
        """
        print("Turning off TemperatureControlUnit and cancelling any operation\n")

        self.set_and_pub_self_signed_event(States_SCU.OFF)
        
    def shutdown_button_pressed(self):
        """sends kill signal, runs on a daemon thread"""
        #TODO: BUTTON PRESSED
        self.turn_off_machine() # logic will kill heating threads
        
    def select_coffee_brewing_option(self):
        """ Coffee menu, requests input from user with number associated with coffee
            if valid_request:
            State Transition (SCU): WAITING -> VALID_REQUEST
            triggering:
            State Transition (TCU): OFF -> HEATING
        """
        if self.get_state() == States_SCU.WAITING:
            print(f"\nSelect Coffee, press {self.escape_menu_key} to quit, and a to abort : \n")
            for key in self.available_coffees.keys():
                print(f"{key} - {self.available_coffees[key]}\n", end="")
            self.menu_option = input()
            if self.menu_option == self.escape_menu_key:
                self.turn_off_machine()
            elif self.menu_option in self.available_coffees: 
                self.set_and_pub_self_signed_event(States_SCU.VALID_REQUEST)    
            else:
                print("Invalid coffee selection. Please try again.") 
             
    def serve_coffee(self):
        """Performs Operation. 
            State Transition(SCU): VALID_REQUEST -> WAITING
            triggering:
            State Transition(TCU): READY -> OFF
        """
        if self.menu_option in self.available_coffees: #redundant
            print(f"{self.available_coffees[self.menu_option]} served\n")
            self.set_and_pub_self_signed_event(States_SCU.WAITING)
            self.menu_option = None


def temp_decay(tcu: TemperatureControlUnit):
    """
    Simulates the temperature decay of water when heater is in state OFF or WAITING
    """
    water_temp_after_decay = 0.9 # 90%

    while True:
        if tcu.get_state() == States_TCU.OFF:
            if tcu.temp > tcu.temp_ambient:
                tcu.temp *= water_temp_after_decay
            else:
                tcu.temp = tcu.temp_ambient
            time.sleep(1)



if __name__ == '__main__':
    EDA = EventSystem()
    
    coffee_machine = StateControlUnit(EDA)
    tcu = TemperatureControlUnit(EDA)
    
    coffee_machine.turn_on_machine()
    # shutdown_button = threading.Thread(target=coffee_machine.shutdown_button_pressed, daemon=True)
    # shutdown_button.start()
    water_decay_thread = threading.Thread(target=temp_decay, args=(tcu,), daemon=True)
    water_decay_thread.start()  
    print(f"Water temp: {tcu.temp:0.2f}")
    #TODO: Make it break loop whenever needed
    while coffee_machine.get_state() != States_SCU.OFF:
        coffee_machine.select_coffee_brewing_option()
        print(f"Water temp: {tcu.temp:0.2f}")
        
    print("finished")

    
    