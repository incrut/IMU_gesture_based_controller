### IMU_based_gesture_controller ###

* Quick summary

It is a IMU connected to raspberry pi pico based controller. The controller consists of a multisensor connected to the Raspberry Pi Pico with a Wi-Fi adapter. This Raspberry Pi receives the signal from the multisensor's gyroscope and accelerometer and based on the signal control the Raspberry Pi robot. The signals will include such functions as going forwards and backwards, turning to right or left, stopping the robot and so on.

### Component list ###

| Item | Total |
| ---- | :---: | 
| GoPiGo3 | 1 |
| Li-ion battery pack | 1 |
| Li-ion battery adapter | 1 |
| 2 cell battery pack (AA) | 1 |
| Pololu AltIMU-10 v5 multi-sensor | 1 |
| RaspberryPi Pico W | 1 |
| USB A/USB Micro B Cable 1.8 m | 1 |
| Power cable (Battery - Robot) | 1 |
| BreadBoard | 1 |
| Male to Male Jumper Wire set (10 pieces) | 1 |
| Male to Female Jumper Wire set (10 pieces) | 1 |
| Micro sd card 32GB | 1 |
| Micro sd card Adaptor | 1 |

### How to work with the code ###

* Before you start you need to make sure that your Raspberry Pi Pico W contains all necessary files to run the code (files in the Pico/Pico\_firmware folder) and you have uploaded the firmware to your Pico W (firmware\_picow.uf2 file in the same folder as other necessary files).
* Also make sure that you have all necessary MQTT modules installed (for more instructions see the guideline_for_mqtt.txt file)
* When everything is set go to file /Robot/RasPiGetVal.py and run it on your Raspberry Pi Robot. If in the shell you see a message "Connected to MQTT broker with result code 0" you managed to connect to the Wi-Fi network and the server is running so you are ready to go.
* When the /RasPiGetVal.py script is running go to your Raspberry Pi Pico W and run the script /Pico/imu\_to\_pi.py
* Make sure that you have changed IP string in this file to the corresponding Public IP of the device where the server is running (Raspberry Pi Robot in our case). Also make sure that you have uploaded imu1.py file to the Pico as imu\_to\_pi.py is dependent on it.
* Note that you can upload this script as main.py to the Pico so that it will work automatically.
* When you have both scripts running you are now able to control the robot with your controller. You can tilt it in any direction to move it. You can also make a rapid up-movement with your controller to increase the sensitivity or down-movement to decrease it. Don't worry if your controller was disconnected or powered-off as the robot stops the movement when there are no specific commands.
* When you want to shut down the system you first advised to poweroff Raspberry Pi Pico W (your controller) and after that press ctrl-c in the shell of the RasPiGetVal.py script that is running on your Raspberry Pi Robot to close the server.