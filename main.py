import sys
import os
import subprocess
import threading
import keyboard
import time
import json
import copy
import shutil

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QMenu, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
)


#### CONSTANTS ####
###################

## Paths

localAppData = os.getenv('LOCALAPPDATA')
powerToysSettings = os.path.join(localAppData, 'settings.json')
keyboardManagerSettingsDirPath = os.path.join(localAppData, 'Microsoft', 'PowerToys', 'Keyboard Manager')
powerToysSettingsFilePath = os.path.join(localAppData, 'Microsoft', 'PowerToys', 'settings.json')

# originalFile = "$settingsFolderPath\default.json"
# backupFile = "$settingsFolderPath\default_old.json"
# newFile = "$settingsFolderPath\default.json"


## Data
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


initialData = {
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


## Fixed GUI elements sizes
WINDOW_SIZE = 600
DISPLAY_CONSOLE_HEIGHT = 50
BASIC_BUTTONS_HEIGHT = 40

# Create instance QApplication
app = QApplication([])



class Wc3RemapWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Wc3 Remap")

        # self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.adjustSize()

        ## Data
        self.data = copy.deepcopy(initialData)

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
        self._createCaptureInputButton()
        self._createApplyChangesButton()
        self._createStopRecordingButton()
        self._createStageChangesButton()
        self._createRevertChangesButton()
        self._createResetFactoryDefaultsButton()
        self._createEnableKboardManager()
        self._createDisableKboardManager()
        # self._createTestButton()
        # self._createSaveCombinationButton()


        self.keyState = set()
        self.keyStateList = list()
        # self.keyState = list()
        self.sourceRecordedKeys = []
        self.destRecordedKeys = []
        self.previewKeySourceMapsList = []
        self.previewKeyDestMapsList = []
            

    #### Display Elements ####
    ##########################

    def _createMainMenu(self):
        mainMenu = self.menuBar().addMenu("&Menu")
        mainMenu.addAction("&Exit", self.close)
        previewMenu = self.menuBar().addMenu("&Preview_Changes")
        # openPreviewAction = QAction(self._createPreviewWindow, self)
        # previewMenu.addAction(openPreviewAction)
        open_popup_action = QAction("Open Popup", self)
        open_popup_action.triggered.connect(self._createPreviewWindow)
        previewMenu.addAction(open_popup_action)
        helpMenu = self.menuBar().addMenu("&Help")
        helpMenu.addAction("&About", self._createAboutWindow)

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
    
    def _createCaptureInputButton(self):
        self.captureInputsButton = QPushButton("Capture Input")
        self.captureInputsButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.captureInputsButton, 1, 1)
        self.captureInputsButton.clicked.connect(self._startKeyCapture)
    
    def _createStopRecordingButton(self):
        self.stopRecordingButton = QPushButton("Stop Recording")
        self.stopRecordingButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.stopRecordingButton, 1, 2)
        self.stopRecordingButton.clicked.connect(self._stopKeyCapture)
    
    def _createStageChangesButton(self):
        self.stageChangesButton = QPushButton("Stage Changes")
        self.stageChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.stageChangesButton, 2, 0)
        self.stageChangesButton.clicked.connect(self._buildDataJson)

    def _createRevertChangesButton(self):
        self.revertChangesButton = QPushButton("Revert Changes")
        self.revertChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.revertChangesButton, 2, 1)
        self.revertChangesButton.clicked.connect(self._revertDataChanges)
    
    def _createResetFactoryDefaultsButton(self):
        self.resetFactoryDefaultsButton = QPushButton("Reset Factory Defaults")
        self.resetFactoryDefaultsButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.resetFactoryDefaultsButton, 2, 2)
        self.resetFactoryDefaultsButton.clicked.connect(self._revertToFactoryDefaults)

    def _createApplyChangesButton(self):
        self.applyChangesButton = QPushButton("Apply Changes")
        self.applyChangesButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.applyChangesButton, 5, 0, 1, -1)
        self.applyChangesButton.clicked.connect(self._applyChanges)
    
    def _createEnableKboardManager(self):
        self.enableKboardManager = QPushButton("Enable Keyboard Manager")
        self.enableKboardManager.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.enableKboardManager, 6, 0, 1, -1)
        self.enableKboardManager.clicked.connect(self._enableKeyboardManager)

    def _createDisableKboardManager(self):
        self.disableKboardManager = QPushButton("Disable Keyboard Manager")
        self.disableKboardManager.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.disableKboardManager, 7, 0, 1, -1)
        self.disableKboardManager.clicked.connect(self._disablePowerToysServices)

    # def _createClearButton(self):
    #     self.clearButton = QPushButton("Test_Button")
    #     self.clearButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
    #     self.wc3AppLayout.addWidget(self.clearButton, 4, 1)
    #     self.clearButton.clicked.connect(self._convertToKeyCodes)

    def _createTestButton(self):
        self.testButton = QPushButton("Test_Button")
        self.testButton.setFixedHeight(BASIC_BUTTONS_HEIGHT)
        self.wc3AppLayout.addWidget(self.testButton, 4, 1)
        self.testButton.clicked.connect(self._applyChanges)

    
    
    

    #### Functionality ####
    #######################  ## To Do add preview changes before applying, REVERT CHANGES WORKS ONLY FOR STAGING PHASE SHOULD ADD A BUTTON TO RESET TO FACTORY DEFAULT REMAPS, space does not work when capturing Add when enable and disable powerytoys a message to display


    def _installPowerToys(self):
        command = ["winget", "install", "--disable-interactivity", "--id", "Microsoft.PowerToys", "--source", "winget"]
        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Check if the command was successful
        if result.returncode == 0:
            self.display.setText("PowerToys installed successfully!")
            self.display.setStyleSheet("font-weight: bold;")
            # print("PowerToys installed successfully!")
            # print(result.stdout)  # Output from the command
        else:
            self.display.setText(f"Failed to install PowerToys. Error code: {result.returncode}")
            self.display.setStyleSheet("font-weight: bold;")
            print(f"Failed to install PowerToys. Error code")
            # print(result.stderr)  # Error output from the command
    

    def _startKeyCapture(self):
        self.display.setText("Press keys (Click Stop Recording to stop)...")
        self.display.setStyleSheet("font-weight: bold;")
        self.keyState.clear()
        keyboard.hook(self._captureKeys)  # Start capturing key events

    def _captureKeys(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            # if not self.sourceRecordedKeys:
            time.sleep(0.20)
            self.keyState.add(event.name.lower()) ## Using set to have unique keys
            self.keyStateList = list(self.keyState)
            # self.keyStateList.sort()
            # self.keyState.append(event.name.lower())  # Add the key to the set
            self.display.setText(f"Press Keys: {', '.join(self.keyStateList)}")
            self.display.setStyleSheet("font-weight: bold;")
            # elif not self.destRecordedKeys:
            #     self.destRecordedKeys.append(event.name.lower())  # Add the key to the set
            #     self.display.setText(f"Dest Keys pressed: {', '.join(self.keyState)}")
    
    def _stopKeyCapture(self):
        if not self.sourceRecordedKeys:
            self.previewKeySourceMapsList.append(self.keyState.copy())
            self.sourceRecordedKeys = self.keyState.copy()
            self.display.setText(f"Source Keys pressed: {' + '.join(self.sourceRecordedKeys)}")
            self.display.setStyleSheet("font-weight: bold;")
            self.keyState.clear()
        else:
            self.previewKeyDestMapsList.append(self.keyState.copy())
            self.destRecordedKeys = self.keyState.copy()
            self.display.setText(f"Dest Keys pressed: {' + '.join(self.destRecordedKeys)}")
            self.display.setStyleSheet("font-weight: bold;")
            self.keyState.clear()
        self.waitingForKey = False  # Stop capturing keys

        keyboard.unhook_all()  # Unhook any keyboard hooks
        

    def _buildDataJson(self):
        # Get the corresponding integer values from the key_codes dictionary
        self.sourceKeyCodes = [str(key_codes[key]) for key in self.sourceRecordedKeys]
        self.destKeyCodes = [str(key_codes[key]) for key in self.destRecordedKeys]
        print(self.sourceKeyCodes, self.destKeyCodes)
        print(f"Source Keys codes: {";".join(self.sourceKeyCodes)}")
        print(f"Dest Keys codes: {";".join(self.destKeyCodes)}")

        # new_entries = [{"originalKeys": ";".join(self.sourceKeyCodes), "newRemapKeys": ";".join(self.destKeyCodes)}] ## Ithink it is wrong and should be the source keys to newRemapKeys
        new_entries = [{"originalKeys": ";".join(self.destKeyCodes), "newRemapKeys": ";".join(self.sourceKeyCodes)}]


        self.data["remapShortcuts"]["global"].extend(new_entries)

        ## Clean keys arrays
        self.sourceRecordedKeys.clear()
        self.destRecordedKeys.clear()

        json_data = json.dumps(self.data, indent=2)

        # Print the updated JSON
        print(json_data)


    def _revertDataChanges(self):
        self.data = initialData
        self.display.setText(f"Buttons changes have been reseted.")
        self.display.setStyleSheet("font-weight: bold;")
        json_data = json.dumps(self.data, indent=2)

        self.previewKeySourceMapsList.clear()
        self.previewKeyDestMapsList.clear()

        # Print the updated JSON
        print(json_data)
        

    def _applyChanges(self):
        newKeyMapFile = "./default.json"

        # Writing to JSON file
        with open(newKeyMapFile, 'w') as json_file:
            json.dump(self.data, json_file, indent=2)
        
        if os.path.isdir(keyboardManagerSettingsDirPath):
            ## Build default.json path
            sourceJsonPath = os.path.join(keyboardManagerSettingsDirPath, "default.json")
            if os.path.exists(sourceJsonPath):
                backupJsonPath = os.path.join(keyboardManagerSettingsDirPath, "default_old.json")
                os.rename(sourceJsonPath, backupJsonPath)
                shutil.copyfile(newKeyMapFile, sourceJsonPath)
    
    def _revertToFactoryDefaults(self):
        self.data = initialData
        self.display.setText(f"Buttons changes have been reseted.")
        self.display.setStyleSheet("font-weight: bold;")
        json_data = json.dumps(self.data, indent=2)

        defaultKeyMapFile = "./default.json"

        # Writing to JSON file
        with open(defaultKeyMapFile, 'w') as json_file:
            json.dump(self.data, json_file, indent=2)

        sourceJsonPath = os.path.join(keyboardManagerSettingsDirPath, "default.json")
        if os.path.exists(sourceJsonPath):
            os.remove(sourceJsonPath)
            shutil.copyfile(defaultKeyMapFile)

    def _disablePowerToysServices(self):
        
        with open(powerToysSettingsFilePath, 'r') as powerToysSettings:
            json_data = json.load(powerToysSettings)
        
        for service in json_data['enabled']:
            json_data['enabled'][service] = False
            data = json.dumps(json_data, indent=2)
            print(data)
            # print(service)
        
        for systemStartup in json_data:
            if systemStartup == 'startup':
                json_data['startup'] = False 

        with open(powerToysSettingsFilePath, 'w') as powerToysSettings: ## Test it if it works
            json.dump(json_data, powerToysSettings, indent=2)
        
        try:
            # Run the 'tasklist' command to get all running processes
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            os.system(f"taskkill /IM PowerToys.exe /F")
            # Print the output, which contains the list of processes
            # print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving processes: {e}")


    def _enableKeyboardManager(self):
        with open(powerToysSettingsFilePath, 'r') as powerToysSettings:
            json_data = json.load(powerToysSettings)
        
            for service in json_data['enabled']:
                if service == 'Keyboard Manager':
                    json_data['enabled'][service] = True
        
        with open(powerToysSettingsFilePath, 'w') as powerToysSettings:
            json.dump(json_data, powerToysSettings, indent=2)
            data = json.dumps(json_data, indent=2)
            print(data)

            # try:
            #     # Run the 'tasklist' command to get all running processes
            #     result = subprocess.run(["tasklist"], capture_output=True, text=True)
            #     os.system(f"taskkill /IM PowerToys.exe /F")
            #     # Print the output, which contains the list of processes
            #     print(result.stdout)
            # except subprocess.CalledProcessError as e:
            #     print(f"Error retrieving processes: {e}")
        time.sleep(5)    

        try:
            # Run the .exe file
            result = subprocess.Popen([r'C:\Users\looma\AppData\Local\PowerToys\PowerToys.exe'])
            print(result)
        except Exception as err:
            print(err)
    

    def _createPreviewWindow(self):
        # Function to create the popup window
        # popupWindow = PopupWindow()  # Create an instance of the PopupWindow
        # popupWindow.show
        previewWindow = QMessageBox(self)
        text = ""
        if len(self.previewKeySourceMapsList) != 0 and len(self.previewKeyDestMapsList) != 0:
            for i in range(len(self.previewKeySourceMapsList)):
                set1 = self.previewKeySourceMapsList[i]
                set2 = self.previewKeyDestMapsList[i]
                set1 = list(set1)
                set2 = list(set2)

                # Join each set into a string for both lists and format it
                text += f'{" + ".join(set1)}      >      {" + ".join(set2)}\n'

        # Set the message box text to the constructed string
        previewWindow.setText(text)
        previewWindow.setStyleSheet("font-weight: bold;")
        # Join each sublist into a string, and add a newline after each list
            # text += f'Key Maps: {", ".join(keyCombination)}\n'
        # previewWindow.setText(text)
        previewWindow.exec()

    def _createAboutWindow(self):
        # Function to create the popup window
        # popupWindow = PopupWindow()  # Create an instance of the PopupWindow
        # popupWindow.show
        aboutWindow = QMessageBox(self)
        text = """To remap your keys, follow these steps:
            Step 1: Capture Input
                Click the "Capture Input" button.
                Press the native key or key combination that you want to change.
                Click "Stop Recording" once you’ve captured the native input.

            Step 2: Capture the Replacement Key
                Click "Capture Input" again to begin capturing the key or key combination you want to use as a replacement.
                Press the new key or combination you wish to assign.
                Click "Stop Capture" to finalize your selection.

            Step 3: Stage Changes
                Click the "Stage Changes" button. This is a crucial step that prepares the changes for preview.

            Step 4: Preview Changes
                Use the menu bar preview to see the changes you’re about to make. This lets you confirm that everything looks correct.

            Step 5: Revert Changes (if needed)
                If you want to discard the changes and start over, click the "Revert Changes" button.

            Step 6: Apply Changes
                If you’re satisfied with the changes, click the "Apply Changes" button. This will save your changes to the Keyboard Manager JSON file.

            Step 7: Enable Keyboard Manager
                After applying the changes, click the "Enable Keyboard Manager" button to activate the remapped keys.

            Step 8: Disable Keyboard Manager
                Once you finish your gaming session, click the "Disable Keyboard Manager" button to restore the default keyboard settings.

            Additional Options
                Factory Reset: If you want to delete all changes and restore the Keyboard Manager file to its original state, click the "Factory Reset" button. This will remove any customizations and replace the current JSON file with the native one.

            4. Enabling and Disabling the Keyboard Manager
                To enable the remapped keys for your gaming session:
                    Click the "Enable Keyboard Manager" button in the main interface.
                After finishing your gameplay session, you can disable the Keyboard Manager:
                    Click the "Disable Keyboard Manager" button to turn off the custom shortcuts and restore your keyboard to default settings

            5. Exiting the Program
                To exit the WC3KeyRemap application:
                    Click on the "Exit" button.
            """
                    

        # Set the message box text to the constructed string
        aboutWindow.setText(text)
        aboutWindow.setStyleSheet("font-weight: bold;")
        # Join each sublist into a string, and add a newline after each list
            # text += f'Key Maps: {", ".join(keyCombination)}\n'
        # previewWindow.setText(text)
        aboutWindow.exec()
            


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


# powerTools = {
#   "startup": true,
#   "enabled": {
#     "AdvancedPaste": false,
#     "AlwaysOnTop": false,
#     "Awake": false,
#     "CmdNotFound": false,
#     "ColorPicker": false,
#     "CropAndLock": false,
#     "EnvironmentVariables": false,
#     "FancyZones": false,
#     "File Explorer": true,
#     "File Locksmith": false,
#     "FindMyMouse": false,
#     "Hosts": false,
#     "Image Resizer": false,
#     "Keyboard Manager": true,
#     "Measure Tool": false,
#     "MouseHighlighter": false,
#     "MouseJump": false,
#     "MousePointerCrosshairs": false,
#     "MouseWithoutBorders": false,
#     "NewPlus": false,
#     "Peek": false,
#     "PowerRename": false,
#     "PowerToys Run": false,
#     "QuickAccent": false,
#     "RegistryPreview": false,
#     "Shortcut Guide": false,
#     "TextExtractor": false,
#     "Video Conference": false,
#     "Workspaces": false
#   },
#   "is_elevated": false,
#   "run_elevated": false,
#   "show_new_updates_toast_notification": true,
#   "download_updates_automatically": true,
#   "show_whats_new_after_updates": true,
#   "enable_experimentation": true,
#   "is_admin": true,
#   "enable_warnings_elevated_apps": true,
#   "theme": "system",
#   "system_theme": "dark",
#   "powertoys_version": "v0.85.1"
# }