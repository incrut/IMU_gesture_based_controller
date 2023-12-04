import paho.mqtt.client as mqtt
from get_ip import get_my_ip
import subprocess
import easygopigo3 as go
import time


data = None


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code", rc) # result code 0-connected / 5-unable to connect
    client.subscribe("pico/data")

def on_message(client, userdata, msg):
    global data
    data = msg.payload.decode()
    print("Received data:", data)

def main():
    global data
    myRobot = go.EasyGoPiGo3()
    myRobot.set_speed(400)    
    
    ip_data = get_my_ip()
    MQTT_BROKER = str(ip_data[2][5:]) # Public IP of the device where mqtt server is running (IP of RasPi in our case)  # "ddd.dd.ddd.d"
    MQTT_USERNAME = "RasPiName" # The username of the RasPi (it was set for the mqtt server manually) sudo mosquitto_passwd -c /etc/mosquitto/passwd your_username
    MQTT_PASSWORD = "RobotPass" # The password for the RasPi username (was also set for the mqtt server manually)
    
    # Run the mqtt server
    print("Opening the server")
    subprocess.run(["sudo", "systemctl", "start", "mosquitto"])
    subprocess.run(["sudo", "systemctl", "enable", "mosquitto"])
    print("Server is open \n")
    
    # Connection to the server
    print("Connecting to the server \n")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Set the MQTT username and password
    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

    client.connect(MQTT_BROKER, 1883, 60)
#     client.loop_forever()
    
    new_iteration = time.time() # Calculate the initialisation time
    prev_iteration = new_iteration    
    
    # Reading the server until Ctrl-C is pressed, after that close the server using console commands
    try:
        while True:
            client.loop(.01) # Blocks for 100ms when set to 0.1
            if data is not None:
                command = data.split()
                left = float(command[0])
                right = float(command[1])
                myRobot.set_motor_dps(myRobot.MOTOR_LEFT, left)
                myRobot.set_motor_dps(myRobot.MOTOR_RIGHT, right)  
                data = None
                prev_iteration = new_iteration # Reset the timer for the no-data counter (so it does not stop every 3 seconds)
                
            # When there is no data on the server
            else:
                new_iteration = time.time() # Count the time when robot has no data given from the server
                if new_iteration - prev_iteration >= 3: # If no command is sent within 3 sec stop the robot
                    myRobot.steer(0,0)
                    prev_iteration = new_iteration # Reset the timer
                    print("No commands are sent for more than 3 seconds")
                    
    except KeyboardInterrupt:
        myRobot.steer(0,0)
        print("Closing the server")
        subprocess.run(["sudo", "systemctl", "stop", "mosquitto"])
        subprocess.run(["sudo", "systemctl", "disable", "mosquitto"])
        print("Server is closed \n")
        

if __name__ == "__main__":
    main()
    
