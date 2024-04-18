import csv
import time
import serial
import serial.tools.list_ports
from threading import Thread
import keyboard  # To detect keyboard inputs

# Global variables
current_label = "1"
stop_recording = False  # Flag to control the recording loop
sep = True  # Initialize sep as a global variable

def get_serial_port() -> serial.tools.list_ports_common.ListPortInfo:
    """
    Returns the port/device of the first connected Arduino.234cc56cc7234c5678q234c5678q2345678cq
    """
    device = None
    time.sleep(0.5)

    while not device:
        devices = serial.tools.list_ports.comports()
        for device in devices:
            if device.vid == 12346:  # Example: Espressif USB VendorID
                if "DC:DA:0C" in device.hwid:
                    print("TinyML board found")
                    return device.device
                else:
                    print("This does not seem to be a TinyML board")
            else:
                print("No device found, waiting..")
                time.sleep(2.5)
    return None

def change_label():
    global current_label, stop_recording, sep  # Declare sep as global here
    while not stop_recording:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'q':
                    stop_recording = True
                    break
                elif event.name.isdigit():
                    current_label = event.name
                    print(f"Label changed to {current_label}")
                    sep = True
                elif event.name == 'c':
                    delete_last_lines('data.csv', 100)
                    print("Last 100 lines deleted from CSV.")
        except KeyboardInterrupt:
            stop_recording = True
            break

def delete_last_lines(filename, lines_to_delete):
    # Open the file in read+write mode without truncating it ('r+').
    with open(filename, 'r+', newline='') as file:
        # Read all rows from the CSV file.
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

        # Check if the number of rows is greater than the number of lines to delete.
        if len(rows) > lines_to_delete:
            # Position the file pointer at the beginning of the file.
            file.seek(0)

            # Write all but the last specified number of lines back to the file.
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows[:-lines_to_delete])

            # Truncate the file to remove any leftover data beyond the new end.
            file.truncate()
        else:
            # If there are not enough rows, optionally handle this case (e.g., notify the user).
            print("Not enough rows to delete the specified number of lines.")

def record_data(device: str, baudrate: int = 9600, filename: str = 'data.csv'):
    global current_label, stop_recording, sep  # Declare sep as global here
    ser = serial.Serial(port=device, baudrate=baudrate)

    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)

        print("Starting to record data.. Press a number to change the label. Press 'q' to stop.\n")

        # Start a separate thread to listen for label changes
        label_thread = Thread(target=change_label)
        label_thread.start()
        counter = 1
        while not stop_recording:
            data = ser.readline().decode('utf-8').strip()
            if data:  # Ensure data is not empty
                print(data)
                if counter == 100:
                    sep = True
                    counter = 1
                csv_writer.writerow(data.split(',') + ['Label: ' + current_label, 'Sep: ' + str(sep)])
                counter = counter + 1
                if sep:
                    sep = False

        ser.close()
        label_thread.join()

        print("\nRecording stopped and data saved.")

if __name__ == '__main__':
    try:
        port = get_serial_port()
        if port:
            record_data(port, baudrate=9600, filename='data.csv')
        else:
            print("Serial port not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
