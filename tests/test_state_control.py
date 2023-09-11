from unittest import mock
import pytest
import pytest_bdd
from pytest_bdd import given, when, then, parsers
from functools import partial

from state_control_unit.StateControlUnit import StateControlUnit
from states_enum.States import States_SCU, States_TCU


scenario = partial(pytest_bdd.scenario, "state_control.feature")


@pytest.fixture()
def state_unit():
    return StateControlUnit()


@scenario("Transition from OFF to WAITING")
def transition_off_waiting():
    pass

# this is kinda nice and all, but following features steps like this is kinda 
# challenging as it is not ordered
@given(parsers.parse("the scu state is initially {state}"))
def initial_state(state_unit, state):
    state = eval("States_SCU."+state)
    if state == States_SCU.OFF:
        assert state_unit.get_state() == States_SCU.OFF
    else:
        assert state_unit.set_state(state) == state


# @given("the scu state is initially OFF")
# def initial_state(state_unit):
#     assert state_unit.get_state() == States_SCU.OFF


@when("the scu is turned on")
def turning_scu_on(state_unit):
    state_unit.turn_on_machine()


@then("scu transitions to WAITING")
def waiting_state(state_unit):
    assert state_unit.get_state() == States_SCU.WAITING


@scenario("Transition from WAITING to VALID_REQUEST or WAITING (if valid or invalid choice)")
def test_transition_waiting_to_valid_request(state_unit):
    pass


# @given("the scu state is initially WAITING")
# def initial_state(state_unit):
#     assert state_unit.set_state(States_SCU.WAITING) == States_SCU.WAITING

@when(parsers.parse("the user selects a coffee brewing option, ex: {number}"))
def select_correct_choice(state_unit, number):
    with mock.patch('builtins.input', return_value=number):
        state_unit.select_coffee_brewing_option()

# without the features by side , this kinda makes the code hard to follow
@then(parsers.parse("scu transitions to {state}"))  
def transition_to_valid_request(state_unit, state):
    msg = state_unit.get_state()
    test_state = eval("States_SCU."+state)
    if isinstance(msg, list):
        assert state_unit.get_state()[0] == test_state
    else:
        assert state_unit.get_state() == test_state
        

@scenario("Transition from WAITING to OFF")
def test_waiting_to_off():
    pass


@when("the scu is turned off")
def turn_off_coffee_machine(state_unit):
    state_unit.turn_off_machine()


@then("the scu should transition to OFF")
def test_if_machine_off(state_unit):
    assert state_unit.get_state() == States_SCU.OFF
    

@scenario("Transition from READY to WAITING")
def test_ready_to_waiting():
    pass


@given("a valid coffee choice")
def coffee_choice(state_unit):
    state_unit.menu_option = "1"
    

@given("the scu receives a READY event")
def receive_event(state_unit):
    state_unit.event_handler(States_TCU.READY)


@when("coffee is served")
def coffee_serve(state_unit):
    state_unit.serve_coffee()
