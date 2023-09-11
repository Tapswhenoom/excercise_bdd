import unittest
from temperature_control_unit.TemperatureControlUnit import TemperatureControlUnit
from states_enum.States import States_TCU
import threading
import time


class TestHardware(unittest.TestCase):

    def setUp(self):
        self.tcu = TemperatureControlUnit()
        self.tcu.set_state(States_TCU.HEATING)
        self.tcu.temp = 20
        self.tcu.temp_desired = 40

    def test_start_heating(self):
        # Start the heating process in a thread
        heating_thread = threading.Thread(target=self.tcu.start_heating)
        heating_thread.start()

        time.sleep(2)

        with self.tcu.temp_lock:
            self.assertGreater(self.tcu.temp, 20)

        self.tcu.set_state(States_TCU.READY)
        heating_thread.join()

    def test_reach_desired_temperature(self):
            
        sensor_thread = threading.Thread(target=self.tcu.reach_desired_temperature)
        sensor_thread.start()

        with self.tcu.temp_lock:
            self.assertGreater(self.tcu.temp_desired, self.tcu.temp)
            self.assertEqual(self.tcu.get_state(), States_TCU.HEATING)
            self.tcu.temp = 50
            self.assertLessEqual(self.tcu.temp_desired, self.tcu.temp)
         
        sensor_thread.join()
        self.assertEqual(self.tcu.get_state(), States_TCU.READY)   

if __name__ == '__main__':
    unittest.main()