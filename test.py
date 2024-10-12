import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QVBoxLayout, QLabel, QDialog, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt  # Import Qt for alignment flags

class PopupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Popup Window")
        self.setGeometry(100, 100, 250, 100)

        # Create a label to display text
        label = QLabel("This is a popup window!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)

        # Layout for the popup window
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)

        # Create a menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create a 'File' menu
        file_menu = QMenu("File", self.menu_bar)

        # Create a menu item to open the popup
        open_popup_action = QAction("Open Popup", self)
        open_popup_action.triggered.connect(self.open_popup)  # Connect the action to the method

        # Add the menu item to the file menu
        file_menu.addAction(open_popup_action)

        # Add the file menu to the menu bar
        self.menu_bar.addMenu(file_menu)

    def open_popup(self):
        popup = PopupWindow()  # Create an instance of the PopupWindow
        popup.exec()  # Show the popup window

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create an instance of QApplication
    main_window = MainWindow()  # Create the main window
    main_window.show()  # Show the main window
    sys.exit(app.exec())  # Start the application
