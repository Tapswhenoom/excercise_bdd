
from  TemperatureControlUnit.TemperatureControlUnit import State
import pytest, logging, time 
from unittest.mock import Mock,patch
from pytest_bdd import given, when, then, scenario ,parsers



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
    logging.info('user turns ON the machine ')

@then('the machine is switeched to IDLE')
def machine_in_idle(temperature_unit):
    assert temperature_unit.get_state() == State.IDLE 
    logging.info(f'the machine is switeched to  {State.IDLE}')

# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from IDLE to HEATING")
def test_transition_from_idle_to_heating():
    pass

@given("machine in IDLE")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.IDLE) 
    logging.info('machine in IDLE ')
    
@when(parsers.parse('the user selects a coffee {option}'))
def select_brew_option(temperature_unit,option):
    temperature_unit.client.publish=Mock()
    logging.info(f'the user selects a coffee  {option} ')
    temperature_unit.select_coffee_brewing_option(option)
    logging.info(f'the state {temperature_unit.get_state()}')
    

@then("the machine is switeched to HEATING")
def transition_to_heating(temperature_unit):
    assert temperature_unit.get_state() == State.HEATING
    logging.info(f'the machine is switeched to {State.HEATING}')
    


# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from HEATING to READY")
def test_transition_from_heating_to_ready():
    pass

@given("machine in HEATING")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.HEATING) 
    logging.info('machine in HEATING ')

# boundary test for temperature   
@when("once target temperature is reashed")
def reashe_desired_temperature(temperature_unit):
    
    temperature_unit.current_temp=70
    temperature_unit.target_temp=70
    logging.info(f'target temperature is {temperature_unit.target_temp}')
    temperature_unit.reach_desired_temperature()
    logging.info(f'target temperature is reached {temperature_unit.target_temp}')
    logging.info(f'machine should switch to Ready')


@then("the machine is switeched to READY")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.READY
    logging.info(f'the machine is switeched to {temperature_unit.get_state()}')



# Define a pytest-bdd scenario
@scenario('../features/temperature_control.feature', "Transition from READY to IDLE")
def test_transition_from_READY_to_IDLE():
    pass

@given("machine in READY")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.READY) 
    logging.info(f'machine in READY')
    
@when("operation finished")
def operation_finished(temperature_unit):
    temperature_unit.client.publish=Mock()
    logging.info(f'Start calculate the wait of 10s')
    time_before = time.time()
    temperature_unit.finish_operation()
    time_after = time.time()
    time_taken = time_after - time_before
    assert time_taken >= 10
    

@then("the machine is switeched to IDLE")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.IDLE
    logging.info(f'operation finished , machine back to {temperature_unit.get_state()} after 10s ')

@scenario('../features/temperature_control.feature', "Transition from IDLE to OFF")
def test_transition_from_IDLE_to_OFF():
    pass

@given("machine in IDLE")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.IDLE) 
    logging.info(f'machine in IDLE ')
    
@when("user turn off the machine")
def operation_finished(temperature_unit):
    temperature_unit.turn_off()
    logging.info(f'user turn off the machine')

@then("the machine is switeched to OFF")
def transition_to_READY(temperature_unit):
    assert temperature_unit.get_state() == State.OFF
    logging.info(f'the machine is switeched to {temperature_unit.get_state()} ')




@scenario('../features/temperature_control.feature', "Transition from HEATING to ERROR")
def test_transition_from_Heating_to_ERROR():
    pass

@when("timeout reached")
def tomeout_reached(temperature_unit):
    with patch('time.sleep'):
        print("Current state:", temperature_unit.get_state())
        temperature_unit.wait_for_finish_coffee_brewing()

#boundary test for temperature   
@when("target temperature is not reached")
def temperature_is_not_reached(temperature_unit):
    temperature_unit.current_temp=69
    temperature_unit.target_temp=70
    temperature_unit.reach_desired_temperature()
    assert temperature_unit.get_state() == State.HEATING
    logging.info(f'target temperature is not reached')
    
    
@then("the machine is switeched to ERROR")
def transition_to_error(temperature_unit):
    assert temperature_unit.get_state() == State.ERROR
    logging.info(f'the machine is switeched to {temperature_unit.get_state()}')

@scenario('../features/temperature_control.feature', "Transition to OFF")
def test_transition_to_OFF():
    pass

@given(parsers.parse("machine in {state}"))
def initial_state(temperature_unit,state):
    temperature_unit.set_state(state) 
    logging.info(f'machine in {state} ')

@scenario('../features/temperature_control.feature', "Transition from ERROR to IDLE")
def test_transition_from_ERROR_to_IDLE():
    pass

@given("machine in ERROR")
def initial_state(temperature_unit):
    temperature_unit.set_state(State.ERROR)
    logging.info(f'machine in  ERROR')
    
@when("user dismiss the error")
def operation_finished(temperature_unit):
    temperature_unit.dismiss_error()
    logging.info(f'user dismiss the error')

@scenario('../features/temperature_control.feature', "Normal Operation-Successful Heating")
def test_normal_operation():
    pass
@scenario('../features/temperature_control.feature', "Timeout During Heating")
def test_invalid_option():
    pass
@scenario('../features/temperature_control.feature', "Immediate Turn Off")
def test_timeout_during_heating():
    pass

@scenario('../features/temperature_control.feature', "Transition from Error After Handling")
def test_transition_from_error_after_handling():
    pass

@scenario('../features/temperature_control.feature', "Choosing an Invalid Option")
def test_invalid_option():
    pass

@when(parsers.parse('user choose an invalid option "{option}"'))
def invalid_option(temperature_unit,option):
    temperature_unit.client.publish=Mock()
    logging.info(f'the user selects a coffee  {option} ')
    temperature_unit.select_coffee_brewing_option(option)
    
    
@then("the machine should not make the caffee")
def transition_to_error(temperature_unit):
    assert temperature_unit.get_state() == State.IDLE

