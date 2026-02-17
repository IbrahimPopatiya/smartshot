from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import webbrowser
from app.licensing.activate_dialog import ActivateLicenseDialog


BUY_URL = "https://your-website.com/buy"  # change later


class TrialExpiredDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("SmartShot – Trial Expired")
        self.setFixedSize(360, 160)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        title = QLabel("Your free trial has ended")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")

        message = QLabel(
            "Thank you for trying SmartShot.\n\n"
            "To continue using all features,\n"
            "please purchase a license."
        )
        message.setAlignment(Qt.AlignCenter)

        buy_btn = QPushButton("Buy License")
        activate_btn = QPushButton("Activate License")
        exit_btn = QPushButton("Exit")

        buy_btn.clicked.connect(self.open_buy_page)
        activate_btn.clicked.connect(self.activate_license)
        exit_btn.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(buy_btn)
        btn_layout.addWidget(activate_btn)
        btn_layout.addWidget(exit_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(message)
        layout.addSpacing(12)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def open_buy_page(self):
        webbrowser.open(BUY_URL)

    def activate_license(self):
        dialog = ActivateLicenseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.accept()
    
