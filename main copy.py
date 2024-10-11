# hello.py

"""Simple Hello, World example with PyQt6."""

import sys
import subprocess
import threading
import keyboard



# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

key_codes = {
    "backspace": 8,
    "tab": 9,
    "enter": 13,
    "ShiftKey": 16,
    "ControlKey": 17,
    "menu": 18,
    "Pause": 19,
    "caps lock": 20,
    "esc": 27,
    "space": 32,
    "page up": 33,
    "page down": 34,
    "end": 35,
    "home": 36,
    "left": 37,
    "up": 38,
    "right": 39,
    "down": 40,
    "Select": 41,
    "Print": 42,
    "Execute": 43,
    "PrintScreen": 44,
    "insert": 45,
    "delete": 46,
    "Help": 47,
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    "a": 65,
    "b": 66,
    "c": 67,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "l": 76,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "v": 86,
    "w": 87,
    "x": 88,
    "y": 89,
    "z": 90,
    "left windows": 91,
    "RWin": 92,
    "Apps": 93,
    "Sleep": 95,
    "NumPad0": 96,
    "NumPad1": 97,
    "NumPad2": 98,
    "NumPad3": 99,
    "NumPad4": 100,
    "NumPad5": 101,
    "NumPad6": 102,
    "NumPad7": 103,
    "NumPad8": 104,
    "NumPad9": 105,
    "Multiply": 106,
    "Add": 107,
    "Separator": 108,
    "Subtract": 109,
    "Decimal": 110,
    "Divide": 111,
    "f1": 112,
    "f2": 113,
    "f3": 114,
    "f4": 115,
    "f5": 116,
    "f6": 117,
    "f7": 118,
    "f8": 119,
    "f9": 120,
    "f10": 121,
    "f11": 122,
    "f12": 123,
    "f13": 124,
    "f14": 125,
    "f15": 126,
    "f16": 127,
    "f17": 128,
    "f18": 129,
    "f19": 130,
    "f20": 131,
    "f21": 132,
    "f22": 133,
    "f23": 134,
    "f24": 135,
    "num lock": 144,
    "Scroll": 145,
    "shift": 160,
    "right shift": 161,
    "ctrl": 162,
    "right ctrl": 163,
    "alt": 164,
    "right alt": 165,
}

# 2. Create an instance of QApplication
app = QApplication([])

## Fixed window size
WINDOW_SIZE = 600
DISPLAY_CONSOLE_HEIGHT = 50
BASIC_BUTTONS_HEIGHT = 40

class Wc3RemapWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Wc3 Remap")

        # self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.adjustSize()

        ## Layout Setup
        self.wc3AppLayout = QGridLayout()

        ## Central Widgets
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.wc3AppLayout)
        self.setCentralWidget(centralWidget)
        

        ## Creating menu bar
        self._createMainMenu()

        ## Creating GUI 
        self._createConsoleDisplay()
        self._createInstallPowerToysButton()
        self._createApplyChangesButton()
        self._createChangeButtonMapButton()
        self._createRevertChangesButton()
        

    #### Display Elements ####
    ##########################

    ## Menu Bar
    def _createMainMenu(self):
        mainMenu = self.menuBar().addMenu("&Menu")
        mainMenu.addAction("&Exit", self.close)
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction("&About", self.close)

    ## Display 
    def _createConsoleDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_CONSOLE_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.wc3AppLayout.addWidget(self.display, 0, 0, 1, -1)
        
    def _createInstallPowerToysButton(self):
        self.installPowerToysButton = QPushButton("Install MS PowerToys")
        self.installPowerToysButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.installPowerToysButton, 1, 1)
        self.installPowerToysButton.clicked.connect(self._installPowerToys)
    
    def _createApplyChangesButton(self):
        self.applyChangesButton = QPushButton("Apply Changes")
        self.applyChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.applyChangesButton, 1, 2)
        self.applyChangesButton.clicked.connect(self._startKeyCapture)
    
    def _createChangeButtonMapButton(self):
        self.changeButtonMap = QPushButton("Change Button")
        self.changeButtonMap.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.changeButtonMap, 2, 0, 1, -1)
    
    def _createRevertChangesButton(self):
        self.revertChangesButton = QPushButton("Revert Changes")
        self.revertChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.revertChangesButton, 1, 3)

    #### Functionality ####
    #######################

    def _installPowerToys(self):
        command = ["winget", "install", "--disable-interactivity", "--id", "Microsoft.PowerToys", "--source", "winget"]
        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Check if the command was successful
        if result.returncode == 0:
            self.display.setText("PowerToys installed successfully!")
            # print("PowerToys installed successfully!")
            # print(result.stdout)  # Output from the command
        else:
            self.display.setText(f"Failed to install PowerToys. Error code: {result.returncode}")
            print(f"Failed to install PowerToys. Error code")
            # print(result.stderr)  # Error output from the command
    
    def _startKeyCapture(self):
        self.display.setText("Waiting for a key press...")
        self.waitingForKey = True

         # Start a thread to listen for key presses
        keyCaptureThread = threading.Thread(target=self._cleanRecordedEvents)
        keyCaptureThread.start()

    # def _startSourceKeyCapture(self):
    #     self.display.setText("Press source key to remap...")
    #     self.waitingForKey = True

    #      # Start a thread to listen for key presses
    #     keyCaptureThread = threading.Thread(target=self._captureKey)
    #     keyCaptureThread.start()
    
    # def _startDestKeyCapture(self):
    #     self.display.setText("Press source key to remap...")
    #     self.waitingForKey = True

    #      # Start a thread to listen for key presses
    #     keyCaptureThread = threading.Thread(target=self._captureKey)
    #     keyCaptureThread.start()

    # Override the keyPressEvent to capture key events
    # Overriding the keyPressEvent method to capture key codes
    def _captureKey(self):
        # while self.waitingForKey:
        #     # Wait for a key press and get its name
        #     event = keyboard.read_event()
        #     key_code = event.scan_code  # Get the scan code of the key
        #     key_name = event.name  # Get the key name (like 'ctrl', 'alt', 'f1')
        #     self.display.setText(f"WC3 Key Code: {key_codes[key_name]}, Key: {key_name} ")
        #     # if event.event_type == keyboard.KEY_DOWN:
        #     #     key_code = event.scan_code  # Get the scan code of the key
        #     #     key_name = event.name  # Get the key name (like 'ctrl', 'alt', 'f1')
        #     #     self.display.setText(f"Key Code: {key_code}, Key: {key_name}")

        #     # Stop capturing after capturing a key
        #     self.waitingForKey = False
        #     return key_name
        #     # break
        #     #     self.display.setText("Key captured. Press the button to capture another key.")

        while self.waitingForKey:
            recordedEvents = keyboard.record(until='esc', trigger_on_release=False)
            print(recordedEvents)
            # for key_event in recorded_events:
            #     if key_event.event_type == 'up' or 'up' in key_event.event_type:
            #         print("REMOVING EVENT :" , key_event.event_type)
            #         recorded_events.remove(key_event)
            # print(recorded_events)
            self.waitingForKey = False
            return recordedEvents
    
    def _cleanRecordedEvents(self):
        recordedEvents = self._captureKey()
        for keyEvent in recordedEvents:
            if keyEvent.event_type == 'up':
                recordedEvents.remove(keyEvent)
        return recordedEvents
            


        





# layout = QGridLayout()

# layout.addWidget(QPushButton("Button (0, 0)"), 0, 0)

# layout.addWidget(QPushButton("Button (0, 1)"), 0, 1)

# layout.addWidget(QPushButton("Button (0, 2)"), 0, 2)

# layout.addWidget(QPushButton("Button (1, 0)"), 1, 0)

# layout.addWidget(QPushButton("Button (1, 1)"), 1, 1)

# layout.addWidget(QPushButton("Button (1, 2)"), 1, 2)

# layout.addWidget(QPushButton("Button (2, 0)"), 2, 0)

# layout.addWidget(QPushButton("Button (2, 1) + 2 Columns Span"), 2, 1, 1, 2) ## 3rd argument means how many rows the widget will occupy and the 4th argument means how many columns the widget will occupy

# window.setLayout(layout)



def main():

    wc3RemapApp = QApplication([])

    wc3RemapWindow = Wc3RemapWindow()

    wc3RemapWindow.show()

    sys.exit(wc3RemapApp.exec())


if __name__ == "__main__":

    main()



# def get_key_code():
#     print("Press any key to get its key code (press 'ESC' to exit):")
    
#     while True:
#         key = msvcrt.getch()  # Wait for a key press
#         key_code = ord(key)  # Get the ASCII value of the key
#         print(f"Key Code: {key_code}")
        
#         if key_code == 27:  # ASCII code for ESC key
#             print("Exiting...")
#             break

key_codes = {
    "backspace": 8,
    "tab": 9,
    "enter": 13,
    "ShiftKey": 16,
    "ControlKey": 17,
    "menu": 18,
    "Pause": 19,
    "caps lock": 20,
    "esc": 27,
    "space": 32,
    "page up": 33,
    "page down": 34,
    "end": 35,
    "home": 36,
    "left": 37,
    "up": 38,
    "right": 39,
    "down": 40,
    "Select": 41,
    "Print": 42,
    "Execute": 43,
    "PrintScreen": 44,
    "insert": 45,
    "delete": 46,
    "Help": 47,
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    "a": 65,
    "b": 66,
    "c": 67,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "l": 76,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "v": 86,
    "w": 87,
    "x": 88,
    "y": 89,
    "z": 90,
    "left windows": 91,
    "RWin": 92,
    "Apps": 93,
    "Sleep": 95,
    "NumPad0": 96,
    "NumPad1": 97,
    "NumPad2": 98,
    "NumPad3": 99,
    "NumPad4": 100,
    "NumPad5": 101,
    "NumPad6": 102,
    "NumPad7": 103,
    "NumPad8": 104,
    "NumPad9": 105,
    "Multiply": 106,
    "Add": 107,
    "Separator": 108,
    "Subtract": 109,
    "Decimal": 110,
    "Divide": 111,
    "f1": 112,
    "f2": 113,
    "f3": 114,
    "f4": 115,
    "f5": 116,
    "f6": 117,
    "f7": 118,
    "f8": 119,
    "f9": 120,
    "f10": 121,
    "f11": 122,
    "f12": 123,
    "f13": 124,
    "f14": 125,
    "f15": 126,
    "f16": 127,
    "f17": 128,
    "f18": 129,
    "f19": 130,
    "f20": 131,
    "f21": 132,
    "f22": 133,
    "f23": 134,
    "f24": 135,
    "num lock": 144,
    "Scroll": 145,
    "shift": 160,
    "right shift": 161,
    "ctrl": 162,
    "right ctrl": 163,
    "alt": 164,
    "right alt": 165,
}

# key_codes = {
#     "Back": 8,
#     "Tab": 9,
#     "Enter": 13,
#     "ShiftKey": 16,
#     "ControlKey": 17,
#     "Menu": 18,
#     "Pause": 19,
#     "CapsLock": 20,
#     "Escape": 27,
#     "Space": 32,
#     "PageUp": 33,
#     "PageDown": 34,
#     "End": 35,
#     "Home": 36,
#     "Left": 37,
#     "Up": 38,
#     "Right": 39,
#     "Down": 40,
#     "Select": 41,
#     "Print": 42,
#     "Execute": 43,
#     "PrintScreen": 44,
#     "Insert": 45,
#     "Delete": 46,
#     "Help": 47,
#     "0": 48,
#     "1": 49,
#     "2": 50,
#     "3": 51,
#     "4": 52,
#     "5": 53,
#     "6": 54,
#     "7": 55,
#     "8": 56,
#     "9": 57,
#     "A": 65,
#     "B": 66,
#     "C": 67,
#     "D": 68,
#     "E": 69,
#     "F": 70,
#     "G": 71,
#     "H": 72,
#     "I": 73,
#     "J": 74,
#     "K": 75,
#     "L": 76,
#     "M": 77,
#     "N": 78,
#     "O": 79,
#     "P": 80,
#     "Q": 81,
#     "R": 82,
#     "S": 83,
#     "T": 84,
#     "U": 85,
#     "V": 86,
#     "W": 87,
#     "X": 88,
#     "Y": 89,
#     "Z": 90,
#     "LWin": 91,
#     "RWin": 92,
#     "Apps": 93,
#     "Sleep": 95,
#     "NumPad0": 96,
#     "NumPad1": 97,
#     "NumPad2": 98,
#     "NumPad3": 99,
#     "NumPad4": 100,
#     "NumPad5": 101,
#     "NumPad6": 102,
#     "NumPad7": 103,
#     "NumPad8": 104,
#     "NumPad9": 105,
#     "Multiply": 106,
#     "Add": 107,
#     "Separator": 108,
#     "Subtract": 109,
#     "Decimal": 110,
#     "Divide": 111,
#     "F1": 112,
#     "F2": 113,
#     "F3": 114,
#     "F4": 115,
#     "F5": 116,
#     "F6": 117,
#     "F7": 118,
#     "F8": 119,
#     "F9": 120,
#     "F10": 121,
#     "F11": 122,
#     "F12": 123,
#     "F13": 124,
#     "F14": 125,
#     "F15": 126,
#     "F16": 127,
#     "F17": 128,
#     "F18": 129,
#     "F19": 130,
#     "F20": 131,
#     "F21": 132,
#     "F22": 133,
#     "F23": 134,
#     "F24": 135,
#     "NumLock": 144,
#     "Scroll": 145,
#     "LShiftKey": 160,
#     "RShiftKey": 161,
#     "LControlKey": 162,
#     "RControlKey": 163,
#     "LMenu": 164,
#     "RMenu": 165,
# }