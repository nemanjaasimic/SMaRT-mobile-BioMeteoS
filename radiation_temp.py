# DS18B20 Temperature sensor

import time
import os
import glob

def find_ds18b20():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    return device_file

def read_temperature_celcius(sensorName):
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()

    if lines[0].strip()[-3:] != 'YES':
        return None

    temperature_start_pos = lines[1].find('t=')

    if temperature_start_pos == -1:
        return None

    temp_string = lines[1][temperature_start_pos+2:]
    temp_c = float(temp_string) / 1000.0

    return temp_c

sensor_name = find_ds18b20()

while True:
    temp_c = read_temperature_celcius(sensor_name)

    if temp_c == None:
        time.sleep(1)
    else:
        print("Temperature is %.1f C" % (temp_c))
        time.sleep(5)
