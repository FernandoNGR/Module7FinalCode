import pygame
from Player import Player
import pygame
from Player import Player
from main_menu import MainMenu
import serial
import serial.tools.list_ports
from threading import Thread
import time
from tensorflow.keras.models import load_model
import numpy as np

selected_predictions = []
stop_recording = False


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


def record_data(device: str, baudrate: int = 9600):
    global stop_recording
    ser = serial.Serial(port=device, baudrate=baudrate)
    model = load_model(r'C:\Users\Fernando\Downloads\Newfinalproject\Model\LSTM_model.keras')
    data_received = False  # Flag to track if any data has been received
    data_list = []  # Initialize the list to store data
    stop_recording = False

    print("Starting to record data.. \n")

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


def start_serial_communication(self):
    port = get_serial_port()
    if port:
        record_data(port, baudrate=9600, predictions_queue=self.predictions_queue)
    else:
        print("Serial port not found.")


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1250
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ikigai")
        self.player_size = 100
        self.player_speed = 5

        # self.player1_sprite = pygame.image.load(r"Graphics/Sprites/PlayerF1.png").convert_alpha()
        # self.player2_sprite = pygame.image.load(r"Graphics/Sprites/PlayerF1.png").convert_alpha()
        # self.player2_sprite = pygame.transform.flip(self.player2_sprite, True, False)

        self.player1 = Player(self.screen, 100, (self.screen_height - self.player_size) // 2, self.player_size,
                              self.player_speed, [r"Graphics/Sprites/PlayerF1.png", r"Graphics/Sprites/PlayerF2.png",
                                                  r"Graphics/Sprites/PlayerF3.png", r"Graphics/Sprites/PlayerF2.png"])
        self.player2 = Player(self.screen, self.screen_width - 100, (self.screen_height - self.player_size) // 2,
                              self.player_size, self.player_speed,
                              [r"Graphics/Sprites/PlayerF1.png", r"Graphics/Sprites/PlayerF2.png",
                               r"Graphics/Sprites/PlayerF3.png", r"Graphics/Sprites/PlayerF2.png"], P2_controls=True)

        self.background_img = pygame.image.load(r'Graphics/Background.png').convert_alpha()

    def run(self):
        main_menu = MainMenu(self.screen)
        main_menu.display()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # self.handle_input()
            self.update(selected_predictions)
            self.draw()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

    def update(self, predict):
        self.predict = predict
        self.player1.update(predict)
        valid = self.player2.update(predict)

        if valid == False:
            selected_predictions.clear()

        self.player1.check_attack_collision(self.player2)
        self.player2.check_attack_collision(self.player1)

        self.player1.is_hit(self.player2)
        self.player2.is_hit(self.player1)

        if self.player1.health_bar.is_dead():
            self.player1.is_dead = True
            self.player1.display_win_screen("Player 2 Wins!")
        if self.player2.health_bar.is_dead():
            self.player2.is_dead = True
            self.player2.display_win_screen("Player 1 Wins!")

        # if self.player1.is_hit(self.player2):
        #     print("Player 2 hit Player 1")
        # #
        # if self.player2.is_hit(self.player1):
        #     print("Player 1 hit Player 2")

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        self.player1.draw()
        self.player2.draw()


if __name__ == "__main__":
    try:
        port = get_serial_port()
        if port:
            game = Game()
            start_thread = Thread(target=record_data, args=(port, 9600))
            start_thread.start()
            game.run()
        else:
            print("Serial port not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
