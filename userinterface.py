import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QProcess


class MediaPlayerControls(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Media Player Controls")
        self.setGeometry(100, 100, 640, 100)

        # Set up the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set background color
        self.central_widget.setStyleSheet("background-color: rgb(45, 45, 45);")

        # Add a layout
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Create a horizontal layout for the media controls
        controls_layout = QHBoxLayout()

        # Path to the directory containing the button icons
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_dir = os.path.join(current_dir, "src")

        # Start the C script as a subprocess
        self.c_process = QProcess(self)
        c_script_path = os.path.join(current_dir, "controls")
        self.c_process.start(c_script_path)

        # Add buttons with callbacks
        self.add_control_button(controls_layout, os.path.join(icon_dir, "small-rewind-backwards.png"), "Small Rewind", "0")
        self.add_control_button(controls_layout, os.path.join(icon_dir, "big-rewind-backwards.png"), "Big Rewind", "1")
        self.add_control_button(controls_layout, os.path.join(icon_dir, "icons8-play-pause-24.png"), "Play/Pause", "2")
        self.add_control_button(controls_layout, os.path.join(icon_dir, "big-rewind-forwards.png"), "Big Forward", "3")
        self.add_control_button(controls_layout, os.path.join(icon_dir, "small-rewind-forwards.png"), "Small Forward", "4")

        # Add the controls layout to the main layout
        layout.addLayout(controls_layout)

    def add_control_button(self, layout, icon_path, tooltip, command):
        """
        Helper method to create a button with an icon, add it to the layout,
        and connect it to send a command to the C script.
        """
        button = QPushButton("", self)
        button.setToolTip(tooltip)  # Optional tooltip
        button.setFixedSize(50, 50)
        button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: transparent;
                background-image: url('{icon_path}');
                background-position: center;
                background-repeat: no-repeat;
            }}
            QPushButton:hover {{
                background-color: lightgray; /* Optional hover effect */
            }}
        """)
        button.clicked.connect(lambda: self.send_command_to_c_process(command))
        layout.addWidget(button)

    def closeEvent(self, event):
        """Ensure the C script process is terminated when the application closes."""
        print("Exiting...")
        self.send_command_to_c_process("5")  # Send the quit command to MPlayer

        # Add a small delay to allow the command to be processed
        self.c_process.waitForBytesWritten(1000)  # Ensure data is written

        if self.c_process.state() == QProcess.Running:
            print("Terminating C process...")
            self.c_process.terminate()
            if not self.c_process.waitForFinished(1000):  # Wait up to 1 second for termination
                print("C process did not terminate, killing it.")
                self.c_process.kill()

        super().closeEvent(event)

    def send_command_to_c_process(self, command):
        """Send a command (e.g., a number) to the C script via stdin."""
        if self.c_process.state() == QProcess.Running:
            self.c_process.write((command + "\n").encode("utf-8"))  # Send the command to the C script
        else:
            print("C process is not running!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MediaPlayerControls()
    main_window.show()
    sys.exit(app.exec_())
