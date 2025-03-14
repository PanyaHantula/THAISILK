import serial
import threading

def read_from_serial(ser):
    """ Continuously read data from the serial port and display it. """
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"\nReceived: {data}")
        except Exception as e:
            print(f"Error reading serial: {e}")
            break

def main():
    port = "/dev/tty.PL2303G-USBtoUART11140"
    baud_rate = "9600"

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Start a separate thread to continuously read from the serial port
    thread = threading.Thread(target=read_from_serial, args=(ser,), daemon=True)
    thread.start()

if __name__ == "__main__":
    main()
