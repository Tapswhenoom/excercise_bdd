from temperature_control_unit.TemperatureControlUnit import TemperatureControlUnit
from temperature_control_unit.StateControlUnit import StateControlUnit

import pytest
from pytest_bdd import given, when, then, scenario


@pytest.fixture()
def state_control_unit():
    return StateControlUnit()

