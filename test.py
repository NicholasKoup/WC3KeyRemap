import sys
import subprocess
import threading
import keyboard
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QGridLayout

key_codes = {
    "backspace": 8,
    "tab": 9,
    "enter": 13,
    "ShiftKey": 16,
    "ControlKey": 17,
    "menu": 18,
    "caps lock": 20,
    "esc": 27,
    "space": 32,
    "a": 65,
    "b": 66,
    "c": 67,
    # Add other keys as needed...
}

# Create an instance of QApplication
app = QApplication([])

class Wc3RemapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wc3 Remap")
        self.setFixedSize(600, 400)

        # Layout Setup
        self.wc3AppLayout = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.wc3AppLayout)
        self.setCentralWidget(centralWidget)

        # GUI Elements
        self.display = QLineEdit()
        self.display.setFixedHeight(40)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.wc3AppLayout.addWidget(self.display, 0, 0, 1, -1)

        self.captureButton = QPushButton("Capture Keys")
        self.captureButton.clicked.connect(self._startKeyCapture)
        self.wc3AppLayout.addWidget(self.captureButton, 1, 0)

        self.keyState = set()  # To track currently pressed keys

    def _startKeyCapture(self):
        self.display.setText("Press keys (Esc to stop)...")
        self.keyState.clear()
        keyboard.hook(self._on_key_event)  # Start capturing key events

    def _on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            self.keyState.add(event.name)  # Add the key to the set
            self.display.setText(f"Currently pressed: {', '.join(self.keyState)}")
        elif event.event_type == keyboard.KEY_UP:
            self.keyState.discard(event.name)  # Remove the key from the set
            self.display.setText(f"Currently pressed: {', '.join(self.keyState)}")

        # Check for specific combinations (e.g., Shift + A)
        if 'shift' in self.keyState and 'a' in self.keyState:
            self.display.setText("Shift + A is pressed!")

def main():
    wc3RemapApp = QApplication([])
    wc3RemapWindow = Wc3RemapWindow()
    wc3RemapWindow.show()
    sys.exit(wc3RemapApp.exec())

if __name__ == "__main__":
    main()