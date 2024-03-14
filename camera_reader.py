import serial
import time
import os


def take_photos():
    serial_port = "/dev/ttyACM0"
    baud_rate = 500_000
    try:
        ser = serial.Serial(
            port = serial_port,
            baudrate = baud_rate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS
        )

        print(":: Connected to serial port:", serial_port)

        counter = 0
        limit = 2
        
        image_data = bytearray()
        
        while True:
            if(counter == limit):
                print("*** Process Completed ***")
                ser.close()
                break
            
            if ser.in_waiting <= 0:
                # NOTE: just restart the loop if there is no data waiting
                continue
            
            print(":: Wait until Vsync is Detected...")
            
            data = ser.read(ser.in_waiting)
            # INFO: check if the current data contains the Vsync signal
            if b'Vsync' in data:
                print(":: Vsync Detected!")
                print("-> Recording Bytes until Frame is Detected")
                while True:
                    data = ser.read(ser.in_waiting)
                    # INFO: check if the current data contains the Frame signal
                    if b'Frame ' in data:
                        print(":: Frame Detected")
                        frame_byte_index = data.index(b'Frame ')
                        print(":: Frame Count: -> ", data[frame_byte_index:frame_byte_index+10].decode())
                        # INFO: save all the bytes before the Frame signal
                        image_data.extend(data.split(b"Frame ")[0])
                        break
                    else:
                        image_data.extend(data)
                open(f"image_{counter}.bin", 'wb').write(image_data)
                image_data.clear()
                counter += 1
            else:
                os.system('clear')
                print("-"*50)
                print(":: Vsync not detected | ",end="")
                print(time.strftime("%H:%M:%S", time.localtime()))

    except serial.SerialException as e:
        print(":: Error connecting to serial port:", e)
