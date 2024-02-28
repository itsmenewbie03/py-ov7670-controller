from camera_reader import take_photos
from ultrasonic_sensor_reader import read_ultrasonic_sensor


def read_all_sensors():
    take_photos()
    read_ultrasonic_sensor()

read_all_sensors()
