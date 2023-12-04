import subprocess
import re
import easygopigo3 as go
import time


def get_my_ip():
    ### Function returns a tuple with time-date when was used, local ip of the device and the public ip ###
    
    ip = subprocess.run(["ip", "a"], capture_output = True, text = True) # Run a linux command window "ip a" command
    stringed_ip = str(ip.stdout) # Convering result to a string

    date = subprocess.run(["date"], capture_output = True, text = True) # Run a linux command window "date" command
    stringed_date = str(date.stdout) # Converting result to a string

    matches = re.findall(r"inet \d+\.\d+\.\d+\.\d+", stringed_ip) # Searching for the inet ip pattern (output is two ip's: local and public)
    
    return [stringed_date, matches[0], matches[1]]

 
def main():
    time.sleep(20) # Waiting some time (20 sec) for computer and all connections to set up
    myRobot = go.EasyGoPiGo3() 
    myRobot.open_eyes() # Using the GoPiGo3 robot eyes blue colour to detect the process has started
    time.sleep(0.5)
    myRobot.close_eyes()
    time.sleep(0.5)
    myRobot.open_eyes()
    time.sleep(0.5)
    myRobot.close_eyes()
    time.sleep(0.5)
    myRobot.open_eyes()
    time.sleep(0.5)
    myRobot.close_eyes()
    
    
    subprocess.run(["sudo", "ufw", "enable"]) # Enable the firewall
    subprocess.run(["sudo", "ufw", "allow", "22"]) # Allow SSH
    subprocess.run(["sudo", "ufw", "allow", "5900"]) # Allow VNC (port 5900)
    subprocess.run(["sudo", "ufw", "reload"]) # Reload UFW to apply the new rules

    ip_info = get_my_ip()

    try:
        f = open("/media/pi/FlashDrive/robot/ip_req.txt", "a") # Opening a text file on the USB flash drive
    except:
        try:
            f = open("/media/pi/FlashDrive/robot/ip_req.txt", "x") # Create a text file if it does not exit on the flash drive
        except:
            print("Device is not connected")
            exit()

    f.write("Date of request: " + str(ip_info[0]))
    f.write("Local IP: " + str(ip_info[1][5:])  + "\n")
    f.write("Public IP: "+ str(ip_info[2][5:])  + "\n")
    f.write("\n")

    f.close()

    print(ip_info[0])
    print([ip_info[1], ip_info[2]])

    f = open("/media/pi/FlashDrive/robot/ip_req.txt", "r")
    print(f.read())
    f.close()
    
    
    # Using the GoPiGo3 robot eyes purple colour to detect the process has ended
    myRobot.set_eye_color((255,0,70)) 
    myRobot.open_eyes()
    time.sleep(0.5)
    myRobot.close_eyes()
    time.sleep(0.5)
    myRobot.open_eyes()
    time.sleep(0.5)
    myRobot.close_eyes()
    time.sleep(0.5)
    myRobot.open_eyes()
    time.sleep(0.5)
    myRobot.close_eyes()

if __name__ == "__main__":
    main()
