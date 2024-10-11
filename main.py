# hello.py

"""Simple Hello, World example with PyQt6."""

import sys
import subprocess
import threading
import keyboard
import time
import json


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
    ")": 48,
    "1": 49,
    "!": 49,
    "2": 50,
    "@": 50,
    "3": 51,
    "#": 51,
    "4": 52,
    "$": 52,
    "5": 53,
    "%": 53,
    "6": 54,
    "^": 54,
    "7": 55,
    "&": 55,
    "8": 56,
    "*": 56,
    "9": 57,
    "(": 57,
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
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
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
        self._createStopRecordingButton()
        self._createTestButton()
        # self._createSaveCombinationButton()


        # self.keyState = set()
        self.keyState = list()
        self.sourceRecordedKeys = []
        self.destRecordedKeys = []
        

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
        self.wc3AppLayout.addWidget(self.installPowerToysButton, 1, 0)
        self.installPowerToysButton.clicked.connect(self._installPowerToys)
    
    def _createApplyChangesButton(self):
        self.applyChangesButton = QPushButton("Capture Buttons")
        self.applyChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.applyChangesButton, 1, 1)
        self.applyChangesButton.clicked.connect(self._startKeyCapture)
    
    def _createChangeButtonMapButton(self):
        self.changeButtonMap = QPushButton("Change Button")
        self.changeButtonMap.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.changeButtonMap, 3, 0, 1, -1)

    # def _createClearButton(self):
    #     self.clearButton = QPushButton("Test_Button")
    #     self.clearButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
    #     self.wc3AppLayout.addWidget(self.clearButton, 4, 1)
    #     self.clearButton.clicked.connect(self._convertToKeyCodes)

    def _createTestButton(self):
        self.testButton = QPushButton("Test_Button")
        self.testButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.testButton, 4, 1)
        self.testButton.clicked.connect(self._convertToKeyCodes)

    def _createStopRecordingButton(self):
        self.stopRecordingButton = QPushButton("Stop Recording")
        self.stopRecordingButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.stopRecordingButton, 1, 2)
        self.stopRecordingButton.clicked.connect(self._stopKeyCapture)
    
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
        self.display.setText("Press keys (Esc to stop)...")
        self.keyState.clear()
        keyboard.hook(self._captureKeys)  # Start capturing key events

    def _captureKeys(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            # if not self.sourceRecordedKeys:
            # self.keyState.append(event.name.lower())  # Add the key to the set
            time.sleep(0.15)
            self.keyState.append(event.name.lower())  # Add the key to the set
            self.display.setText(f"Press Keys: {', '.join(self.keyState)}")
            # elif not self.destRecordedKeys:
            #     self.destRecordedKeys.append(event.name.lower())  # Add the key to the set
            #     self.display.setText(f"Dest Keys pressed: {', '.join(self.keyState)}")
    
    def _stopKeyCapture(self):
        if not self.sourceRecordedKeys:
            self.sourceRecordedKeys = self.keyState.copy()
            self.display.setText(f"Source Keys pressed: {' + '.join(self.sourceRecordedKeys)}")
            self.keyState.clear()
        else:
            self.destRecordedKeys = self.keyState.copy()
            self.display.setText(f"Dest Keys pressed: {' + '.join(self.destRecordedKeys)}")
            self.keyState.clear()
        self.waitingForKey = False  # Stop capturing keys

        keyboard.unhook_all()  # Unhook any keyboard hooks
        # self.source_saved_combination = ' + '.join(self.sourceRecordedKeys)
        # self.dest_saved_combination = ' + '.join(self.destRecordedKeys)

        # print(f"Source Saved Combination: {self.source_saved_combination}, Dest Saved Combination: {self.dest_saved_combination}")
        # self.display.setText("Key capture stopped.")

    def _convertToKeyCodes(self):
        # Get the corresponding integer values from the key_codes dictionary
        self.sourceKeyCodes = [str(key_codes[key]) for key in self.sourceRecordedKeys]
        self.destKeyCodes = [str(key_codes[key]) for key in self.destRecordedKeys]
        print(self.sourceKeyCodes, self.destKeyCodes)
        print(f"Source Keys codes: {";".join(self.sourceKeyCodes)}")
        print(f"Dest Keys codes: {";".join(self.destKeyCodes)}")

        data = {
            "remapKeys": {
                "inProcess": []
            },
            "remapKeysToText": {
                "inProcess": []
            },
            "remapShortcuts": {
                "global": [],
                "appSpecific": []
            },
            "remapShortcutsToText": {
                "global": [],
                "appSpecific": []
            }
        }
        new_entries = [{"originalKeys": ";".join(self.sourceKeyCodes), "newRemapKeys": ";".join(self.destKeyCodes)}]

        data["remapShortcuts"]["global"].extend(new_entries)

        json_data = json.dumps(data, indent=2)

        # Print the updated JSON
        print(json_data)




def main():

    wc3RemapApp = QApplication([])

    wc3RemapWindow = Wc3RemapWindow()

    wc3RemapWindow.show()

    sys.exit(wc3RemapApp.exec())


if __name__ == "__main__":

    main()



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
    ")": 48,
    "1": 49,
    "!": 49,
    "2": 50,
    "@": 50,
    "3": 51,
    "#": 51,
    "4": 52,
    "$": 52,
    "5": 53,
    "%": 53,
    "6": 54,
    "^": 54,
    "7": 55,
    "&": 55,
    "8": 56,
    "*": 56,
    "9": 57,
    "(": 57,
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
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
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
