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

def parse_rfid_data(buffer):
    start_marker = b'\xe0\xf8'
    end_marker = b'~'

    while True:
        start_index = buffer.find(start_marker)
        if start_index == -1:
            return None, buffer

        end_index = buffer.find(end_marker, start_index)
        if end_index == -1:
            return None, buffer

        frame = buffer[start_index:end_index + 1]
        buffer = buffer[end_index + 1:]
        return frame, buffer

def extract_uid(frame):
    # Asumimos que el UID está en una posición específica dentro del frame
    # Esto puede variar según la especificación del tag y el protocolo utilizado
    # Ajusta los índices según la estructura exacta de tus datos
    return frame[4:12]  # Ejemplo: extrayendo bytes específicos como UID

while True:
    try:
        if ser.in_waiting > 0:
            buffer = ser.read(ser.in_waiting)
            print('Buffer (raw bytes):', buffer)
            
            frame, buffer = parse_rfid_data(buffer)
            if frame:
                uid = extract_uid(frame)
                print('Parsed RFID Tag UID:', uid.hex())
            else:
                print('Failed to parse RFID data or waiting for more data.')
    except serial.SerialException as e:
        print(f"Serial Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    time.sleep(0.1)
