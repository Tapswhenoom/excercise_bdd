import pytest , time ,threading
from unittest.mock import Mock, patch
import paho.mqtt.client as mqtt
from  TemperatureControlUnit.TemperatureControlUnit import State



class TestTemperatureTimeout:
    
    def test_temperature_reached_timeout_not_reached(self,temperature_unit):
        temperature_unit.set_state(State.HEATING)
        def temperature_thread():
            temperature_unit.current_temp=10
            temperature_unit.target_temp=30
            time.sleep(9)
            temperature_unit.current_temp=temperature_unit.target_temp
            temperature_unit.reach_desired_temperature()
        def timeout_thread():
            temperature_unit.coffee_brewing_timeout=10
            temperature_unit.wait_for_finish_coffee_brewing()
        
        temp_thread = threading.Thread(target=temperature_thread)
        time_thread = threading.Thread(target=timeout_thread)
        temp_thread.start()
        time_thread.start()
        temp_thread.join()
        assert temperature_unit.get_state()== State.READY
        time_thread.join()
        assert temperature_unit.get_state()== State.IDLE

    def test_temperature_not_reached_and_timout_reached(self,temperature_unit): 
        temperature_unit.set_state(State.HEATING)
        def temperature_thread():
            temperature_unit.current_temp=10
            temperature_unit.target_temp=30
            time.sleep(11)
            temperature_unit.current_temp=temperature_unit.target_temp
            temperature_unit.reach_desired_temperature()
        def timeout_thread():
            temperature_unit.coffee_brewing_timeout=10
            temperature_unit.wait_for_finish_coffee_brewing()
        
        temp_thread = threading.Thread(target=temperature_thread)
        time_thread = threading.Thread(target=timeout_thread)
        temp_thread.start()
        time_thread.start()
        temp_thread.join()
        assert temperature_unit.get_state()== State.ERROR
        time_thread.join()
        assert temperature_unit.get_state()== State.ERROR


