import time
import socket
import paho.mqtt.client as mqtt

class State:
        OFF="OFF"
        IDLE = "IDLE"
        HEATING = "HEATING" 
        READY = "READY"
        ERROR = "ERROR" 

class HeatingTimeoutException(Exception):
    pass
class TemperatureControlUnit:
    def __init__(self):
        self.state = State.OFF
        self.coffee_brewing_timeout=60
        self.target_temp = 25
        self.current_temp=0
        self.time_after_ready=10
        self.broker_address = "mqtt_broker" #host name of MQTT broker 
        self.port = 1883 #port of MQTT broker
        self.topic_target_temp = "target_temp" # the subscribe topic for the requested temperature from  Control Unit 
        self.topic_current_temp = "current_temp" # the publish topic for current temperature read from temperature sensore  
        self.topic_heater_state = "heater_state"
        self.client = mqtt.Client() #initialize MQTT client
        self_heater_state='OFF'
        
        self.coffee_options = ["Espresso","Cappuccino","Latte","Black_Coffee"]
        
        

    def publish_temperature(self):
        self.client.publish(self.topic_target_temp, self.target_temp, qos=1)
        print(f"Published  Target Temperature: {self.target_temp} °C")


    def subscribe_current_tempurature(self):
        self.client.subscribe(self.topic_current_temp)
        self.client.on_message = self.on_message
        self.client.loop_start()

                 
    def on_message(self, client, userdata, message):
        if message.topic == self.topic_current_temp:
            self.current_temp =int(message.payload.decode())
            print(f"Received message on topic '{self.topic_current_temp}': {self.current_temp}")
            self.reach_desired_temperature()
    
    
    def connect_to_broker(self):
        while True:
            try:
                self.client.connect(self.broker_address, self.port) #connect to MQTT Broker
                print('connected to Broker successfully')
                break
            except (socket.gaierror, ConnectionRefusedError )as e:
                print('Could not connect to Broker , retrying')
                time.sleep(2) 


    def get_state(self):
        return self.state
    
    def set_state(self,state):
        self.state=state
        print(f'machine status {self.state}')

    def turn_on(self):
        if self.state == State.OFF:
            self.set_state(State.IDLE)
    

    def turn_off(self):
        self.turn_off_heater()
        self.set_state(State.OFF)

        

    def select_coffee_brewing_option(self,option):
        if self.state == State.IDLE:
            if option in self.coffee_options:
                print(f"Selected {option}. Coffee maker is now heating.")
                self.set_state(State.HEATING)
                self.start_heating(temp=40)
            
        
    def start_heating(self,temp):
        if self.state == State.HEATING:
            # Simulate the heating process
            # In a real embedded system, this might involve interacting with hardware
            self.turn_on_heater(temp)
            
            # self.set_state(State.HEATING)

    def turn_on_heater(self,temp):
        self.set_target_temp(temp)
        self.client.publish(self.topic_heater_state, 'ON', qos=1)

    def turn_off_heater(self):
        print('turn_off_heater')
        self.client.publish(self.topic_heater_state, 'OFF', qos=1)
       
            
    def reach_desired_temperature(self):
        if self.state == State.HEATING:
            # if self.target_temp[0] <= self.current_temp <= self.target_temp[1] :
            if self.target_temp <=self.current_temp:
                print(f'desired temperature reached {self.state}')
                self.set_state(State.READY)
    
    def wait_for_finish_coffee_brewing(self):
        try:
            for second in range(self.coffee_brewing_timeout):
                if self.state==State.HEATING:
                    time.sleep(1)
                elif self.state=='READY':
                    break 
            print(f'finished time out waiting , machine state is {self.state}')
            if self.state==State.HEATING:
                raise  HeatingTimeoutException
            self.finish_operation()
        except HeatingTimeoutException:
            print("timelimit is reached, the caffee is not heated properly")
            self.handle_error()
    

    def handle_error(self):
        if self.state==State.HEATING:
            self.set_state(State.ERROR)
            self.turn_off_heater()

    def finish_operation(self):
        self.turn_off_heater()
        if self.state == State.READY:
            time.sleep(self.time_after_ready)
        self.set_state(State.IDLE)

    def dismiss_error(self):
        if self.state==State.ERROR:
            print('user dismmis the error')
            self.set_state(State.IDLE)

    def set_target_temp(self,target_temp):
        self.target_temp=target_temp
        print(f'target temp set to {self.target_temp}')
        self.publish_temperature()
    
        

if __name__ == "__main__":
    temperature_control_unit=TemperatureControlUnit()
    temperature_control_unit.connect_to_broker()
    temperature_control_unit.subscribe_current_tempurature()
    time.sleep(10)
    temperature_control_unit.turn_on()
    temperature_control_unit.select_coffee_brewing_option("Cappuccino")
    temperature_control_unit.wait_for_finish_coffee_brewing()
    if temperature_control_unit.get_state()==State.ERROR:
        temperature_control_unit.dismiss_error()
    temperature_control_unit.select_coffee_brewing_option("Latte")
    temperature_control_unit.wait_for_finish_coffee_brewing()
    if temperature_control_unit.get_state()==State.ERROR:
        temperature_control_unit.dismiss_error()
    temperature_control_unit.turn_off()
    while True:
        pass
    


