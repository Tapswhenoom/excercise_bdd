import pytest,logging,pytest_bdd

from TemperatureControlUnit.TemperatureControlUnit import TemperatureControlUnit , State



def pytest_html_report_title(report):
    report.title = "Coffee Maker testResults"

# Define a fixture to create an instance of TemperatureControlUnit
@pytest.fixture
def temperature_unit():
    logging.info('Initialize and return an instance of TemperatureControlUnit')
    return TemperatureControlUnit()


# pytest_bdd.parsers.parse = pytest.mark.parametrize
# # Use a hook to provide a custom marker for BDD features
def pytest_configure(config):
    config.addinivalue_line("markers", "negative: mark a test as a negative test")
