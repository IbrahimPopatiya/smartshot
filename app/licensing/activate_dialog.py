from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from app.licensing.license_manager import activate_license


class ActivateLicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Activate SmartShot")
        self.setFixedSize(360, 170)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        title = QLabel("Enter your license key")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")

        self.input = QLineEdit()
        self.input.setPlaceholderText("XXXX-XXXX-XXXX")
        self.input.setAlignment(Qt.AlignCenter)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: red;")

        activate_btn = QPushButton("Activate")
        cancel_btn = QPushButton("Cancel")

        activate_btn.clicked.connect(self.try_activate)
        cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(activate_btn)
        btns.addWidget(cancel_btn)
        btns.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(self.input)
        layout.addWidget(self.status)
        layout.addSpacing(8)
        layout.addLayout(btns)

        self.setLayout(layout)

    def try_activate(self):
        key = self.input.text()

        if activate_license(key):
            self.accept()
        else:
            self.status.setText("Invalid license key")
