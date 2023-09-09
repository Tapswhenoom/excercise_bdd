from enum import Enum


class TemperatureControlUnitState(Enum):
    OFF = "OFF"
    HEATING = "HEATING"
    READY = "READY"


class TemperatureControlUnit:
    def __init__(self):
        self.state: TemperatureControlUnitState = TemperatureControlUnitState.OFF

    def get_state(self) -> TemperatureControlUnitState:
        return self.state

    def select_coffee_brewing_option(self) -> None:
        if self.is_off():
            self.start_heating()

    def start_heating(self) -> None:
        # Simulate the heating process
        # In a real embedded system, this might involve interacting with hardware
        self.set_temperature_state(TemperatureControlUnitState.HEATING)

    def reach_desired_temperature(self) -> None:
        # Simulate reaching the desired temperature
        # In a real embedded system, this might involve temperature sensors
        if self.is_heating():
            self.set_temperature_state(TemperatureControlUnitState.READY)

    def set_temperature_state(self, state: TemperatureControlUnitState) -> None:
        if state not in TemperatureControlUnitState:
            raise ValueError(f"'{state}' is not a valid temperature state")

        self.state = state

    def is_off(self):
        return self.get_state() == TemperatureControlUnitState.OFF

    def is_heating(self):
        return self.get_state() == TemperatureControlUnitState.HEATING

    def is_ready(self):
        return self.get_state() == TemperatureControlUnitState.READY
