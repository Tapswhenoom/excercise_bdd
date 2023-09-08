from temperature_control_unit.TemperatureControlUnit import TemperatureControlUnit

import pytest
from pytest_bdd import given, when, then, scenario

# Fixture to create a new instance of TemperatureControlUnit for each scenario
@pytest.fixture
def temperature_unit():
    return TemperatureControlUnit()

# Define a pytest-bdd scenario
@scenario("temperature_control.feature", "Initial state is OFF")
def test_initial_state_off():
    pass

# Define steps for the scenario
@given("the temperature control unit is initially OFF")
def initial_state(temperature_unit):
    assert temperature_unit.get_state() == "OFF"
    
@scenario("temperature_control.feature", "Transition to HEATING")
def test_transition_to_heating():
    pass

@given("the temperature control unit is initially OFF")
def initial_state(temperature_unit):
    assert temperature_unit.get_state() == "OFF"

@when("the user starts the coffee machine")
def turn_machine_on(temperature_unit):
    temperature_unit.turn_on_machine()

@when("the user selects a valid coffee brewing option")
def valid_coffee_choice(monkeypatch,temperature_unit):
    monkeypatch.setattr('builtins.input', lambda _: "9")
    temperature_unit.select_coffee_brewing_option()
    
