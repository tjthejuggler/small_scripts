import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QEventLoop
import time

class MouseModeIndicator(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(MouseModeIndicator, self).__init__(parent)
        self.update_icon()
        self.start_checking()
        self.activated.connect(self.on_tray_icon_clicked)

    def update_icon(self):
        config_file = f'{os.environ["HOME"]}/.config/mouse_toggler'
        with open(config_file, 'r') as f:
            mode = f.read().strip()
        icon_path = '~/projects/small_scripts/'
        icon_path = os.path.expanduser(icon_path)
        if mode == 'right':
            self.setIcon(QIcon(icon_path+'right_mouse_button.png'))
            self.setToolTip('Right Mouse Button Mode')
        else:
            self.setIcon(QIcon(icon_path+'middle_mouse_button.png'))
            self.setToolTip('Middle Mouse Button Mode')

    def start_checking(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_icon)
        self.timer.start(1000) # Update every second

    def on_tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            # Replace 'your_script.sh' with the actual path to your shell script
            script_path = '~/projects/small_scripts/toggle_mouse.sh'
            script_path = os.path.expanduser(script_path)
            subprocess.Popen(['bash', script_path])

if __name__ == '__main__':
    time.sleep(8) # Wait for the system tray to be ready

    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)

    indicator = MouseModeIndicator()
    indicator.show()

    sys.exit(app.exec_())
