import time
import serial

# Configurar el puerto serial
try:
  ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
  print(f'Serial port {ser.port} opened successfully at {ser.baudrate} baud.')
except serial.SerialException as e:
  print(f"Error opening serial port: {e}")
  exit(1)

print('Place tag near the RFID Module for reading (hold for writing)')

buffer = b''

def parse_rfid_data(data):
  start_marker = b'\x18\x18\x00~'
  ## end_marker = b'~'  # Uncomment if your reader uses a specific end marker

  if start_marker in data:
    start_index = data.index(start_marker)
    end_index = len(data)
    if start_index < end_index:
      return data[start_index:end_index].hex()
  return None

def write_uuid_and_protect(uuid):
    # Comando para escribir el UUID en una ubicación específica del chip
    write_command = f"WRITE {00} {uuid}"  # Reemplaza address con la dirección correcta

    # Comando para bloquear el sector
    block_command = "BLOCK {0}"  # Reemplaza sector con el número de sector

    try:
        ser.write(write_command.encode())
        # Esperar confirmación de escritura exitosa
        # ...

        ser.write(block_command.encode())
        # Esperar confirmación de bloqueo exitoso
        # ...
    except serial.SerialException as e:
        print(f"Error al escribir o bloquear el UUID: {e}")
    
def detect_tag_presence_for_duration():
  time.sleep(1)
  return True

while True:
  try:
    if ser.in_waiting > 0:
      buffer += ser.read(ser.in_waiting)
      print('Buffer (raw bytes):', buffer)
      tag_id = parse_rfid_data(buffer)
      if tag_id:
        print('Parsed RFID Tag ID:', tag_id)
        is_tag_present = detect_tag_presence_for_duration()
        if is_tag_present:
          write_uuid_and_protect(tag_id)

        buffer = b''
      else:
        print('Failed to parse RFID data.')
        if len(buffer) > 100:
          buffer = buffer[-100:]
  except serial.SerialException as e:
    print(f"Serial Exception: {e}")
  except Exception as e:
    print(f"Unexpected error: {e}")
  time.sleep(0.1)


