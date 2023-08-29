import pytest,logging,pytest_bdd

from TemperatureControlUnit.TemperatureControlUnit import TemperatureControlUnit

# Define a fixture to create an instance of TemperatureControlUnit
@pytest.fixture
def temperature_unit():
    logging.info('Initialize and return an instance of TemperatureControlUnit')
    return TemperatureControlUnit()


# pytest_bdd.parsers.parse = pytest.mark.parametrize
# # Use a hook to provide a custom marker for BDD features
def pytest_configure(config):
    config.addinivalue_line("markers", "bdd: mark a test as a BDD test")

# # Define a hook to inject the application instance into BDD steps


# @pytest.hookimpl(tryfirst=True)
# def pytest_bdd_before_step(request, feature, scenario, step, step_func):
#     if "temperature_unit" in request.fixturenames:
#         step_func(request.getfixturevalue("temperature_unit"))
# @pytest.hookimpl(tryfirst=True)
# def pytest_bdd_before_step(request, feature, scenario, step, step_func, step_func_args):
#     if "temperature_unit" in request.fixturenames:
#         step_func_args["temperature_unit"] = request.getfixturevalue("temperature_unit")
