from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    show_overlay = pyqtSignal()

