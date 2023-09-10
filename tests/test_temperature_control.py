import pytest
# from pytest_bdd import given, when, then, scenario
import pytest_bdd
from pytest_bdd import given, when, then
from unittest import mock
from functools import partial

from temperature_control_unit.TemperatureControlUnit import TemperatureControlUnit
from states_enum.States import States_TCU, States_SCU


# Fixture to create a new instance of TemperatureControlUnit for each scenario
@pytest.fixture
def temperature_unit():
    return TemperatureControlUnit()

scenario = partial(pytest_bdd.scenario, "temperature_control.feature")


# we could do something like the commented code below, but it makes it harder
# to get what the test is doing, but it does makes it simpler to write
def common_given_initial_state(temperature_unit, initial_state):
    if initial_state == "OFF":
        assert temperature_unit.get_state() == States_TCU.OFF
        

# Define a pytest-bdd scenario
@scenario("Initial state is OFF")
def test_initial_state_off():
    pass

        
# Define steps for the scenario
@given("the temperature control unit is initially OFF")
def initial_state(temperature_unit):
    assert temperature_unit.get_state() == States_TCU.OFF


@scenario("Transition to HEATING")
def test_transition_to_heating():
    pass


@when("the temperature control unit receives an event with a temperature request")
def temperature_request(temperature_unit):
    def new_start_brewing():
        return
    with mock.patch.object(temperature_unit, "start_brewing",
                           new=new_start_brewing):
        temperature_unit.event_handler([States_SCU.VALID_REQUEST, 80])


@then("the temperature control unit should transition to HEATING")
def transition_to_heating(temperature_unit):
    assert temperature_unit.get_state() == States_TCU.HEATING


@scenario("Transition to READY")
def test_transition_to_ready():
    pass


@given("the temperature control unit is initially HEATING")
def initial_state(temperature_unit):
    assert temperature_unit.set_state(States_TCU.HEATING) == States_TCU.HEATING


@when("the temperature reaches the desired temperature")
def reach_desired_temp(temperature_unit):
    temperature_unit.temp = temperature_unit.temp_desired
    temperature_unit.reach_desired_temperature()


@then("the temperature control unit should transition to READY")
def transition_to_ready(temperature_unit):
    assert temperature_unit.get_state() == States_TCU.READY


@scenario("Transition to OFF")
def test_transition_to_off():
    return


@given("the temperature control unit is READY")
def initial_state(temperature_unit):
    assert temperature_unit.set_state(States_TCU.READY) == States_TCU.READY


@when("the temperature control unit receives an event to turn OFF")
def request_off(temperature_unit):
    temperature_unit.event_handler(States_SCU.OFF)


@then("the temperature control unit should transition to OFF")
def transition_to_off(temperature_unit):
    assert temperature_unit.get_state() == States_TCU.OFF


@scenario("Test water heating and sensor logic")
def test_water_logic():
    pass


@given("the temperature control unit receives an event with a temperature request")
def temperature_request(temperature_unit):
    temperature_unit.event_handler([States_SCU.VALID_REQUEST, 80])


@when("the brewing process is called")
def calling_brewing(temperature_unit):
    temperature_unit.start_brewing()


@then("water will reach the needed temp")
def temp_reach(temperature_unit):
    assert temperature_unit.temp >= temperature_unit.temp_desired


@scenario("Transition to OFF waiting for request")
def trans_off_waiting_request():
    pass


@when("the temperature control unit receives an event to wait")
def wait_event(temperature_unit):
    temperature_unit.handle_event(States_SCU.WAITING)


@scenario("Complete loop from the tcu")
def test_loop():
    pass