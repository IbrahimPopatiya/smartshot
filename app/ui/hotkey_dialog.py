from PyQt5.QtCore import Qt
from app.ui.base_dialog import BaseDialog


class HotkeyDialog(BaseDialog):
    def __init__(self):
        super().__init__(
            title="Set Screenshot Hotkey",
            message="Press the key combination you want to use for taking screenshots."
        )

        self.hotkey = None

        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 10pt;")

    def keyPressEvent(self, event):
        parts = []

        if event.modifiers() & Qt.ControlModifier:
            parts.append("ctrl")
        if event.modifiers() & Qt.ShiftModifier:
            parts.append("shift")
        if event.modifiers() & Qt.AltModifier:
            parts.append("alt")

        key = event.key()

        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt):
            return

        key_name = event.text().lower()
        if not key_name:
            key_name = Qt.Key(key).name.replace("Key_", "").lower()

        parts.append(key_name)
        self.hotkey = "+".join(parts)
        self.accept()
