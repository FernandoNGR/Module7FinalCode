import serial
import serial.tools.list_ports
from threading import Thread
import keyboard
import time
from tensorflow.keras.models import load_model
import numpy as np



def get_serial_port() -> str:
    """
    Returns the port/device of the first connected Arduino.
    """
    while True:
        devices = serial.tools.list_ports.comports()
        for device in devices:
            if device.vid == 12346:  # Example: Vendor ID
                if "DC:DA:0C" in device.hwid:
                    print("TinyML board found")
                    return device.device
                else:
                    print("This does not seem to be a TinyML board")
            else:
                print("No device found, waiting..")
                time.sleep(2.5)

def listen_for_stop_command():
    global stop_recording
    while True:
        if keyboard.is_pressed('q'):  # If 'q' is pressed, stop recording
            stop_recording = True
            break
        time.sleep(0.1)  # Short sleep to reduce CPU usage

def record_data(device: str, baudrate: int = 9600):
    global stop_recording
    ser = serial.Serial(port=device, baudrate=baudrate)
    model = load_model('LSTM_model.keras')
    data_received = False  # Flag to track if any data has been received
    data_list = []  # Initialize the list to store data
    selected_predictions = []  # List to store selected predictions (0, 1, 2, 3)
    stop_recording = False
    stop_thread = Thread(target=listen_for_stop_command)
    stop_thread.start()

    print("Starting to record data.. Press 'q' to stop.\n")

    while not stop_recording:
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').strip()
            print(data)  # Debug print to verify raw data
            if data:  # Ensure data is not empty
                if not data_received:
                    last_data_time = time.time()
                    data_received = True
                try:
                    processed_values = [float(value.split(':')[1].strip()) for value in data.split(',')[:3]]
                    if len(processed_values) == 3:
                        data_list.append(np.array(processed_values, dtype=float))
                except Exception as e:
                    print("Error processing data:", e)
        elif data_received and time.time() - last_data_time > 2:
            print("\nNo data received for two seconds.")
            if data_list:
                data_array = np.array(data_list)
                if data_array.shape[0] >= 100:
                    data_array = data_array[:100]
                    data_array = data_array.reshape(1, 100, 3)
                    predictions = model.predict(data_array)
                    predicted_class_index = np.argmax(predictions, axis=1)[0]  # Get the index of max prediction
                    print(int(predicted_class_index))
                    # Check if the predicted class index is one of the desired values and if the list is empty
                    if predicted_class_index == 7:
                        selected_predictions.clear()
                        print("Prediction was '7', list has been reset.")
                    elif len(selected_predictions) == 0 and predicted_class_index in [0, 1, 2, 3]:
                        selected_predictions.append(predicted_class_index)
                        print(f"Added prediction {predicted_class_index} to empty list.")
                    elif len(selected_predictions) == 1 and predicted_class_index in [4, 5, 6]:
                        selected_predictions.append(predicted_class_index)
                        print(f"Added prediction {predicted_class_index} to list with one existing entry.")

                    else:
                        print("No suitable condition to add prediction.")

                    print(selected_predictions)
                else:
                    print("Not enough data collected for a full prediction batch.")
            data_received = False
            data_list = []
            last_data_time = time.time()

    ser.close()
    stop_thread.join()
    print("\nRecording completely stopped. Selected predictions:", selected_predictions)


if __name__ == '__main__':
    try:
        port = get_serial_port()
        if port:
            record_data(port, baudrate=9600)
        else:
            print("Serial port not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
