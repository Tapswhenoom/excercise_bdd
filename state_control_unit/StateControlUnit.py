if __name__ == '__main__':
    import sys
    import os
    # Dependent on file structure
    # Add the parent directory of the current script to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from states_enum.States import States_SCU, States_TCU


class StateControlUnit():  # CoffeeMachine
    def __init__(self, event_system=None):
        self.state = States_SCU.OFF 
        self.event_system = event_system
        if event_system is not None:
            self.event_system.subscribe(self)

        self.available_coffees = {
            "1": {"name" : "Espresso", "temperature_required" : 85},
            "2" : {"name" : "Cappuccino" , "temperature_required" : 90}, 
            "3" : {"name" : "Latte" , "temperature_required" : 80},
            "4" : {"name" : "Americano" , "temperature_required" : 80},
                                  }
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

    def event_handler(self, event):
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
                print(f"{key} - {self.available_coffees[key]['name']}\n", end="")
            
            self.menu_option = input()
            
            if self.menu_option == self.escape_menu_key:
                self.turn_off_machine()
                
            elif self.menu_option in self.available_coffees: 
                msg = [self.set_state(States_SCU.VALID_REQUEST),
                       self.available_coffees[self.menu_option]["temperature_required"]]
                self.set_and_pub_self_signed_event(msg)  
            
            else:
                print("Invalid coffee selection. Please try again.") 
             
    def serve_coffee(self):
        """Performs Operation. 
            State Transition(SCU): VALID_REQUEST -> WAITING
            triggering:
            State Transition(TCU): READY -> OFF
        """
        if self.menu_option in self.available_coffees:
            print(f"{self.available_coffees[self.menu_option]['name']} served\n")
            self.set_and_pub_self_signed_event(States_SCU.WAITING)
            self.menu_option = None


if __name__ == '__main__':
    coffee_machine = StateControlUnit()
    
    coffee_machine.turn_on_machine()
    # shutdown_button = threading.Thread(target=coffee_machine.shutdown_button_pressed, daemon=True)
    # shutdown_button.start()
    # TODO: Make it break loop whenever needed
    while coffee_machine.get_state() != States_SCU.OFF:
        coffee_machine.select_coffee_brewing_option()
        coffee_machine.serve_coffee()
        
    print("finished")
