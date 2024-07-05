import time
import serial

# Configurar el puerto serial
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    print(f'Serial port {ser.port} opened successfully at {ser.baudrate} baud.')
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

print('Place tag near the RFID Module')

def capture_raw_data(buffer):
    with open('raw_data.log', 'ab') as f:
        f.write(buffer)
        f.write(b'\n')

while True:
    try:
        if ser.in_waiting > 0:
            buffer = ser.read(ser.in_waiting)
            capture_raw_data(buffer)  # Guardar los datos crudos para análisis
            print('Buffer (raw bytes):', buffer)
            
            # Aquí iría tu lógica de parseo actual, si es necesario
    except serial.SerialException as e:
        print(f"Serial Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    time.sleep(0.1)







