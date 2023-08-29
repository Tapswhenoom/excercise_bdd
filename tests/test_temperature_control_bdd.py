
from  TemperatureControlUnit.TemperatureControlUnit import State
import pytest, logging, time 
from pathlib import Path
from unittest.mock import Mock,patch
from pytest_bdd import given, when, then, scenario ,parsers



# Fixture to create a new instance of TemperatureControlUnit for each scenario
# @pytest.fixture
# def temperature_unit():
#     temp=TemperatureControlUnit()
#     return temp

# Define steps for the scenario
@given("the temperature control unit is initially OFF")
def initial_state(temperature_unit):
    assert temperature_unit.get_state() == State.OFF
    logging.info('the temperature control unit is initially OFF ')


@scenario('../features/temperature_control.feature', "Transition from OFF to IDLE")
def test_transition_from_OFF_to_IDLE():
    pass

@when('user turns ON the machine')
def turn_on_machine(temperature_unit):
    temperature_unit.turn_on()

@then('the machine is switeched to IDLE')
def machine_in_idle(temperature_unit):
    assert temperature_unit.get_state() == State.IDLE 

# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from IDLE to HEATING")
def test_transition_from_idle_to_heating():
    pass

@given("machine in IDLE")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.IDLE) 
    
@when(parsers.parse('the user selects a coffee {option}'))
def select_brew_option(temperature_unit,option):
    temperature_unit.client.publish=Mock()
    logging.info(f'the user selects a coffee  {option} ')
    temperature_unit.select_coffee_brewing_option(option)
    logging.info(f'the state {temperature_unit.get_state()} ')
    

@then("the machine is switeched to HEATING")
def transition_to_heating(temperature_unit):
    assert temperature_unit.get_state() == State.HEATING


# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from HEATING to READY")
def test_transition_from_heating_to_ready():
    pass

@given("machine in HEATING")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.HEATING) 

    
@when("once target temperature is reashed")
def reashe_desired_temperature(temperature_unit):
    temperature_unit.current_temp=temperature_unit.target_temp
    temperature_unit.reach_desired_temperature()


@then("the machine is switeched to READY")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.READY



# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from READY to IDLE")
def test_transition_from_READY_to_IDLE():
    pass

@given("machine in READY")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.READY) 
    
@when("operation finished")
def operation_finished(temperature_unit):
    temperature_unit.client.publish=Mock()
    time.sleep=Mock()
    temperature_unit.finish_operation()

@then("the machine is switeched to IDLE")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.IDLE

@scenario('../features/temperature_control.feature', "Transition from IDLE to OFF")
def test_transition_from_IDLE_to_OFF():
    pass

@given("machine in IDLE")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.IDLE) 
    
@when("user turn off the machine")
def operation_finished(temperature_unit):
    temperature_unit.turn_off()

@then("the machine is switeched to OFF")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.OFF


@scenario('../features/temperature_control.feature', "Transition from OFF to IDLE to HEATING to READY to IDLE to HEATING to ERROR to IDLE to OFF")
def test_transition_from_OFF_to_OFF():
    pass

@scenario('../features/temperature_control.feature', "Transition from HEATING to ERROR")
def test_transition_from_Heating_to_ERROR():
    pass

@when("timeout reached")
def tomeout_reached(temperature_unit):
    with patch('time.sleep'):
        print("Current state:", temperature_unit.get_state())
        temperature_unit.wait_for_finish_coffee_brewing()


@when("target temperature is not reached")
def temperature_is_not_reached(temperature_unit):
    temperature_unit.current_temp=69
    temperature_unit.target_temp=70
    temperature_unit.reach_desired_temperature()
    assert temperature_unit.get_state() == State.HEATING
    
    
@then("the machine is switeched to ERROR")
def transition_to_error(temperature_unit):
    assert temperature_unit.get_state() == State.ERROR

@scenario('../features/temperature_control.feature', "Transition to OFF")
def test_transition_to_OFF():
    pass

@given(parsers.parse("machine in {state}"))
def initial_state(temperature_unit,state):
    temperature_unit.set_state(state) 

@scenario('../features/temperature_control.feature', "Transition from ERROR to IDLE")
def test_transition_from_ERROR_to_IDLE():
    pass

@given("machine in ERROR")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.ERROR) 
    
@when("user dismiss the error")
def operation_finished(temperature_unit):
    temperature_unit.dismiss_error()

