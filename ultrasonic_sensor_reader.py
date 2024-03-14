import serial
import time
from datetime import timedelta

def read_ultrasonic_sensor():
    port = "/dev/ttyUSB0" 
    baud_rate = 115_200
    
    ser = serial.Serial(port, baud_rate)
    start = time.time()
    data_list = []

    while True:
        if len(data_list) == 10:
            print(":: Process Completed")
            print(data_list)
            print(":: Average Distance:", sum(data_list)/len(data_list))
            break
        
        if ser.in_waiting <= 0:
            continue
        if len(data_list) <= 0:
            end = time.time()
            print(f":: Got data after {timedelta(seconds=int(end)-(start))}")
        
        # TODO: parse the data
        data = ser.read(ser.in_waiting)
        distance = int(data.split(b':')[1].split(b'\r')[0].decode())
        # WARN: this blindly accepts the reading, 
        # WARN: additional calibration must be added to normalize the readings
        data_list.append(distance)

    ser.close()
    open(f"ultrasonic_sensor_data_{time.time()}.txt", "w").write(str(data_list))
    print(":: Data saved to file")
