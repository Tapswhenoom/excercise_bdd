import pytest , time ,threading
from unittest.mock import Mock, patch
import paho.mqtt.client as mqtt
from  TemperatureControlUnit.TemperatureControlUnit import State



class TestTemperatureTimeout:
    
    def test_temperature_reached_timeout_not_reached(self,temperature_unit):
        temperature_unit.set_state(State.HEATING)
        def temperature_thread():
            temperature_unit.current_temp=10
            temperature_unit.target_temp=30
            time.sleep(1)
            temperature_unit.current_temp=temperature_unit.target_temp
            temperature_unit.reach_desired_temperature()
        def timeout_thread():
            temperature_unit.coffee_brewing_timeout=2
            temperature_unit.wait_for_finish_coffee_brewing()
        
        temp_thread = threading.Thread(target=temperature_thread)
        time_thread = threading.Thread(target=timeout_thread)
        temp_thread.start()
        time_thread.start()
        temp_thread.join()
        assert temperature_unit.get_state()== State.READY
        time_thread.join()
        assert temperature_unit.get_state()== State.IDLE

    def test_temperature_not_reached_and_timout_reached(self,temperature_unit): 
        temperature_unit.set_state(State.HEATING)
        def temperature_thread():
            temperature_unit.current_temp=10
            temperature_unit.target_temp=30
            time.sleep(2)
            temperature_unit.current_temp=temperature_unit.target_temp
            temperature_unit.reach_desired_temperature()
        def timeout_thread():
            temperature_unit.coffee_brewing_timeout=1
            temperature_unit.wait_for_finish_coffee_brewing()
        
        temp_thread = threading.Thread(target=temperature_thread)
        time_thread = threading.Thread(target=timeout_thread)
        temp_thread.start()
        time_thread.start()
        temp_thread.join()
        assert temperature_unit.get_state()== State.ERROR
        time_thread.join()
        assert temperature_unit.get_state()== State.ERROR
        # assert temperature_unit.get_state()== State.IDLE



# @pytest.mark.parametrize("target_temp", [25, 30, 35])
# def test_publish_temperature(temperature_unit, target_temp):
#     temperature_unit.target_temp = target_temp
#     assert temperature_unit.publish_temperature()
    # assert temperature_unit.client.publish(temperature_unit.topic_target_temp, target_temp, qos=1)


# def test_on_message(temperature_unit, mqtt_client):
#     message_payload = "25"
#     message = mock.Mock(topic=temperature_unit.topic_current_temp, payload=message_payload.encode())
#     temperature_unit.on_message(mqtt_client, None, message)
#     assert temperature_unit.current_temp == int(message_payload)

# def test_subscribe_current_tempurature(temperature_unit, mqtt_client):
#     temperature_unit.subscribe_current_tempurature()
#     mqtt_client.subscribe.assert_called_once_with(temperature_unit.topic_current_temp)
#     mqtt_client.on_message = temperature_unit.on_message
#     mqtt_client.loop_start.assert_called_once()

# def test_connect_to_broker(temperature_unit, mqtt_client):
#     with mock.patch("time.sleep"):
#         temperature_unit.connect_to_broker()
#         mqtt_client.connect.assert_called_once_with(temperature_unit.broker_address, temperature_unit.port)