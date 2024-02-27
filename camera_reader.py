import serial
import time
import os

# Specify the serial port and baud rate
serial_port = "/dev/ttyACM0"
baud_rate = 500_000

try:
    # Create a serial connection object
    ser = serial.Serial(
        port =serial_port,
        baudrate = baud_rate,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS
    )

    # Print a message indicating successful connection
    print("Connected to serial port:", serial_port)

    # You can now perform serial communication operations using the 'ser' object
    # Example:
    #   ser.write(b"Hello from Python!\n")  # Send data
    counter = 0
    limit = 9
    
    image_data = bytearray()
    read_size = 1024 * 1 
    
    while True:
        if(counter == limit):
            print("byebye")
            ser.close()
            break
        if ser.in_waiting <= 0:
            # NOTE: just restart the loop if there is no data waiting
            continue
        print("Wait until Vsync is Detected")
        
        data = ser.read(ser.in_waiting)
        if b'Vsync' in data:
            # fetch data the might be lost
            print("Vsync deez nuts")
            print("Record Bytes until Frame is Detected")
            while True:
                data = ser.read(ser.in_waiting)
                open(f"dump_{counter}.log","wb").write(data)
                if b'Frame ' in data:
                    frame_byte_index = data.index(b'Frame ')
                    open(f"{counter}.log","w").write(data[frame_byte_index:frame_byte_index+10].decode())
                    print("Frame Count: -> ", data[frame_byte_index:frame_byte_index+10].decode())
                    image_data.extend(data.split(b"Frame ")[0][1:])
                    print("Frame Detected")
                    break
                else:
                    image_data.extend(data)
            open(f"image_{counter}.bin", 'wb').write(image_data)
            image_data.clear()
            counter += 1
        else:
            os.system('clear')
            print("-"*50)
            print("Vsync not detected | ",end="")
            print(time.strftime("%H:%M:%S", time.localtime()))

except serial.SerialException as e:
    print("Error connecting to serial port:", e)
