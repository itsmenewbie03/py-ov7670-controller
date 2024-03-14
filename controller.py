import concurrent.futures
from camera_reader import take_photos
from ultrasonic_sensor_reader import read_ultrasonic_sensor

if __name__ == "__main__":
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    pool.submit(take_photos)
    pool.submit(read_ultrasonic_sensor)
    pool.shutdown(wait=True)
