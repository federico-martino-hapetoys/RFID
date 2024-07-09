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

buffer = b''

def parse_rfid_data(data):
    start_marker = b'~'
    ## end_marker = b'~'

    if start_marker in data:
        start_index = data.index(start_marker)
        end_index = len(data)
        if start_index < end_index:
            return data[start_index:end_index].hex()
    return None

while True:
    try:
        if ser.in_waiting > 0:
            buffer += ser.read(ser.in_waiting)
            print('Buffer (raw bytes):', buffer)
            tag_id = parse_rfid_data(buffer)
            if tag_id:
                print('Parsed RFID Tag ID:', tag_id)
                buffer = b''  # Limpiar el buffer después de una lectura exitosa
            else:
                print('Failed to parse RFID data.')
                # Mantener en el buffer solo los últimos bytes relevantes para intentar ensamblar la trama en la próxima iteración
                if len(buffer) > 100:  # Ajusta este valor según el tamaño esperado de tus tramas
                    buffer = buffer[-100:]
    except serial.SerialException as e:
        print(f"Serial Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    time.sleep(0.1)






