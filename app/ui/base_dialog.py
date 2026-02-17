from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class BaseDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setFixedWidth(360)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # Message
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)

        # Button area
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        layout.addLayout(self.button_layout)

    def add_button(self, text, role="primary"):
        btn = QPushButton(text)
        btn.setFixedHeight(28)
        btn.setMinimumWidth(90)

        if role == "primary":
            btn.setDefault(True)

        self.button_layout.addWidget(btn)
        return btn
