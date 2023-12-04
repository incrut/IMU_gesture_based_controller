#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import machine
import time
from pololu import IMU


def init_IMU():
    # Variable for the multi-sensor object
    global m_sense
    i2c = machine.I2C(id = 0,
                  scl=machine.Pin(1),
                  sda=machine.Pin(0))
    m_sense = IMU(i2c)
    m_sense.barometer_init(IMU.BAROMETER_FREQ_1HZ)
    m_sense.accelerometer_init(IMU.ACCELEROMETER_FREQ_13HZ, IMU.ACCELEROMETER_SCALE_2G)
    m_sense.gyroscope_init(IMU.GYROSCOPE_FREQ_13HZ, IMU.GYROSCOPE_SCALE_125DPS)
    m_sense.magnetometer_init(IMU.MAGNETOMETER_FREQ_1_25HZ, IMU.MAGNETOMETER_SCALE_4GAUSS)
    time.sleep(1)


def get_IMU_values():
    # Constants for sensors
    SENSITIVITY_baro = 4096 # (LSB/hPa)
    SENSITIVITY_accel = 0.061 # (mg/LSB)
    SENSITIVITY_gyro = 4.375  # (mdps/LSB)
    SENSITIVITY_mag = 6842   # (LSB/gauss)
    SENSITIVITY_temp = 16    # (LSB/°C)
    baro_raw = m_sense.barometer_raw_data()
    baro = baro_raw / SENSITIVITY_baro
    accel_raw = m_sense.accelerometer_raw_data()
    accel = [SENSITIVITY_accel * accel_raw["x"], SENSITIVITY_accel * accel_raw["y"], SENSITIVITY_accel * accel_raw["z"]]
    accel = [round(round(i, 2)/1000, 2) for i in accel]
    gyro_raw = m_sense.gyroscope_raw_data()
    gyro = [SENSITIVITY_gyro * gyro_raw["x"], SENSITIVITY_gyro * gyro_raw["y"], SENSITIVITY_gyro * gyro_raw["z"]]
    gyro = [round(round(i, 2)/1000, 2) for i in gyro]
    mag_raw = m_sense.magnetometer_raw_data()
    mag = [mag_raw["x"] / SENSITIVITY_mag, mag_raw["y"] / SENSITIVITY_mag, mag_raw["z"] / SENSITIVITY_mag]
    mag = [round(i, 2) for i in mag]
    temp_raw = m_sense.lsm6ds33_raw_temp()
    temp = 25 + (temp_raw/SENSITIVITY_temp)
    return [baro, accel, gyro, mag, temp]
    
def main():
    init_IMU()
    
    while True:
        IMU_data = get_IMU_values()
        print(f"B: {IMU_data[0]:.2f} hPa")
        print(f"A: {IMU_data[1]} g")
        print(f"G: {IMU_data[2]} dps")
        print(f"M: {IMU_data[3]} gauss")
        print(f"T: {IMU_data[4]:.2f}°C")
        time.sleep(1)
        print("\n")
        
#         print(accel[0],accel[1],accel[2],)
#         time.sleep(0.5)


if __name__ == "__main__":
    main()

