from temperature_control_unit.TemperatureControlUnit import TemperatureControlUnit

from pytest_bdd import given, when, then, scenario


@scenario("temperature_control.feature", "Initial state is OFF")
def test_initial_state_off():
    pass


@given("the temperature control unit is initially OFF")
def initial_state(temperature_unit: TemperatureControlUnit) -> None:
    assert temperature_unit.is_off()


@scenario("temperature_control.feature", "Transition to HEATING")
def test_transition_to_heating() -> None:
    pass


@when("the user selects a coffee brewing option")
def select_brew_option(temperature_unit: TemperatureControlUnit) -> None:
    temperature_unit.select_coffee_brewing_option()


@then("the temperature control unit should transition to HEATING")
def transition_to_heating(temperature_unit: TemperatureControlUnit) -> None:
    assert temperature_unit.is_heating()


@scenario("temperature_control.feature", "Transition to READY")
def test_transition_to_ready() -> None:
    pass


@given("the temperature control unit is HEATING")
def heating_state(temperature_unit: TemperatureControlUnit) -> None:
    temperature_unit.start_heating()
    assert temperature_unit.is_heating()


@when("the water reached the desired temperature")
def water_reach_temperature(temperature_unit: TemperatureControlUnit) -> None:
    temperature_unit.reach_desired_temperature()


@then("the temperature control unit should transition to READY")
def transition_to_ready(temperature_unit: TemperatureControlUnit) -> None:
    assert temperature_unit.is_ready()


@scenario("temperature_control.feature", "Two coffees change nothing")
def test_two_coffee() -> None:
    pass

@then("the temperature control unit should remain in HEATING")
def remains_heating(temperature_unit: TemperatureControlUnit) -> None:
    assert temperature_unit.is_heating()