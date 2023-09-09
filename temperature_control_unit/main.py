from StateControlUnit import StateControlUnit
from TemperatureControlUnit import TemperatureControlUnit, temp_decay
from States import States_SCU, States_TCU

from Event_system import EventSystem

import threading


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