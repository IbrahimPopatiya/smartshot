from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject


class SystemTray(QObject):
    def __init__(self, app, icon_path):
        super().__init__()
        self.app = app

        icon = QIcon(icon_path)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)

        menu = QMenu()
        exit_action = QAction("Exit")
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

        self.tray.showMessage(
            "Screenshot Tool",
            "App is running in background",
            QSystemTrayIcon.Information,
            3000
        )

    def exit_app(self):
        self.tray.hide()
        self.app.quit()

        
    def notify(self, title: str, message: str, duration=3000):
        self.tray.showMessage(
            title,
            message,
            self.tray.Information,
            duration
        )
    
