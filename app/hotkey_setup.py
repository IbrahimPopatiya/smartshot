from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt,QTimer


class HotkeyCaptureDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set Hotkey")
        self.setFixedSize(300, 120)

        self.label = QLabel("Press desired hotkey combination")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.hotkey = None

    def keyPressEvent(self, event):
        parts = []

        if event.modifiers() & Qt.ControlModifier:
            parts.append("ctrl")
        if event.modifiers() & Qt.ShiftModifier:
            parts.append("shift")
        if event.modifiers() & Qt.AltModifier:
            parts.append("alt")

        key = event.key()

        # Ignore modifier-only presses
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt):
            return

        key_name = event.text().lower()
        if not key_name:
            key_name = Qt.Key(key).name.replace("Key_", "").lower()

        parts.append(key_name)

        self.hotkey = "+".join(parts)
        self.label.setText(self.hotkey)

        QTimer.singleShot(300, self.accept)

