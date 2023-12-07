import network
from umqtt.simple import MQTTClient
import machine
from time import sleep
import time
from imu1 import init_IMU
from imu1 import get_IMU_values

WIFI_SSID = "Wi-Fi" # Wi-Fi network to connect. Must be the same as the network where mqtt server is running
WIFI_PASSWORD = "Password"
MQTT_BROKER = "132.85.194.25" # Public IP of the device where mqtt server is running (IP of RasPi in our case)
MQTT_USERNAME = "PicoName" # The username of the Pico (it was set for the mqtt server manually) sudo mosquitto_passwd /etc/mosquitto/passwd your_username
MQTT_PASSWORD = "PicoPass" # The password for the Pico username (was also set for the mqtt server manually)

client = None


def map_range (x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}') # IP of the devise that runs this function (Pico in our case)
    return ip

def connect_mqtt():
    global client
    client = MQTTClient("pi", MQTT_BROKER, user=MQTT_USERNAME, password=MQTT_PASSWORD)
    client.connect()
    print("Connected to MQTT broker")

def publish_data(data):
    client.publish("pico/data", data)
    

def main():
    led = machine.Pin("LED", machine.Pin.OUT) # Onboard LED initialisation
    led.on() # Indication that Pico is powered
    ip = connect_wifi()
    connect_mqtt()
    init_IMU()
    sensitivity = {"HIGH": [-400,400], "LOW": [-100, 100]}
    state = "HIGH"
    
    while True:
        led.on() # Blink with LED to show that function is running
        IMU_data = get_IMU_values()
        print(f"B: {IMU_data[0]:.2f} hPa")
        print(f"A: {IMU_data[1]} g")
        print(f"G: {IMU_data[2]} dps")
        print(f"M: {IMU_data[3]} gauss")
        print(f"T: {IMU_data[4]:.2f}°C")
        
        if IMU_data[1][0] >= 1.5:
            state = "HIGH"
        elif IMU_data[1][0] <= -1.5:
            state = "LOW"
        
        left = map_range (IMU_data[1][1], -1.03, 1.03, sensitivity[state][0], sensitivity[state][1]) - map_range (IMU_data[1][2], -1.03, 1.03, sensitivity[state][0], sensitivity[state][1])
        right = map_range (IMU_data[1][1], -1.03, 1.03, sensitivity[state][0], sensitivity[state][1]) + map_range (IMU_data[1][2], -1.03, 1.03, sensitivity[state][0], sensitivity[state][1])
        data = str(left) + ' ' + str(right)
#         data = IMU_data[1]
        publish_data(str(data))
#         time.sleep(0.1)
        print("\n")
        led.off() # Blink with LED to show that function is running

if __name__ == "__main__":
    main()

