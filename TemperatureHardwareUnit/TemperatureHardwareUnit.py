import time
import socket
import paho.mqtt.client as mqtt


class TemperatureHardwareUnit:
    def __init__(self) -> None: 
        self.target_temp= 25 
        self.room_temp=25 #set Room Temp
        self.current_temp= self.target_temp
        self.broker_address = "mqtt_broker" #host name of MQTT broker 
        self.port = 1883 #port of MQTT broker
        self.topic_target_temp = "target_temp" # the subscribe topic for the requested temperature from  Control Unit 
        self.topic_current_temp = "current_temp" # the publish topic for current temperature read from temperature sensore  
        self.topic_heater_state = "heater_state"
        self.heater_state = "OFF"
        self.client = mqtt.Client() #initialize MQTT client
        self.connect_to_broker()


    def publish_temperature(self):
        self.client.publish(self.topic_current_temp, self.current_temp, qos=1)
        print(f"Published Temperature: {self.current_temp} °C")
        
       

    def temprature_update(self):
        while True:

            if self.heater_state == "ON":
                target_temp=self.target_temp
            elif self.heater_state == "OFF":
                target_temp=self.room_temp
                
            if self.current_temp < target_temp: 
                self.current_temp +=1  # Simulate  increase of temperature
            elif  self.current_temp > target_temp: 
                self.current_temp -=1  # Simulate  decrease of temperature
            self.publish_temperature()
            time.sleep(2)  # Publish every 2 seconds

    

    def subscribe_to_topics(self):
        self.client.subscribe(self.topic_target_temp)
        self.client.subscribe(self.topic_heater_state)
        self.client.on_message = self.on_message
        self.client.loop_start()
    

    def connect_to_broker(self):
        while True: 
            try:
                self.client.connect(self.broker_address, self.port) #connect to MQTT Broker
                print('connected to Broker successfully')
                break
            except (socket.gaierror, ConnectionRefusedError )as e:
                print('Could not connect to Broker , retrying')
                time.sleep(2)
        
            
    def on_message(self, client, userdata, message):
        print(f"Received message on topic '{message.topic}': {message.payload.decode()}")
        if message.topic == self.topic_target_temp:
            self.target_temp =int(message.payload.decode())
            
        elif message.topic == self.topic_heater_state:
            self.heater_state=message.payload.decode()
           



if __name__ == "__main__":
    temperature_hardware_unit=TemperatureHardwareUnit()
    #recieve the  requested temperature from  Control Unit )
    temperature_hardware_unit.subscribe_to_topics()
    #start update and send current temprature 
    temperature_hardware_unit.temprature_update()
    
