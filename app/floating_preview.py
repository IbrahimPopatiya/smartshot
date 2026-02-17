from PyQt5 import QtWidgets, QtGui, QtCore
import os
from app.clipboard import copy_image_to_clipboard
from app.ocr import extract_text_from_image


class FloatingPreview(QtWidgets.QWidget):
    def __init__(self, image_path, position=None):
        super().__init__()

        

        self.image_path = image_path
        self.pixmap = QtGui.QPixmap(image_path)

        self.zoom_factor = 1.0
        self.min_zoom = 0.2
        self.max_zoom = 5.0
        self.original_pixmap = self.pixmap

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )


        self._dragging = False
        self._drag_offset = QtCore.QPoint()

        self._build_ui(position)

    def _build_ui(self, position):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # image
        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # buttons
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()

        copy_btn = QtWidgets.QPushButton("Copy")
        text_btn = QtWidgets.QPushButton("Extract Text")
        close_btn = QtWidgets.QPushButton("Close")

        copy_btn.clicked.connect(self.copy_to_clipboard)
        text_btn.clicked.connect(self.extract_text)
        close_btn.clicked.connect(self.close)

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(text_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.adjustSize()

        if position is not None:
            self.move(position)
        else:
            self.move(200, 200)

        self.show()

    
    # ---------- drag window ----------
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.move(event.globalPos() - self._drag_offset)

    def mouseReleaseEvent(self, event):
        self._dragging = False

    def closeEvent(self, event):
        try:
            from app.main import floating_refs
            floating_refs.remove(self)
        except Exception:
            pass
        event.accept()

    def wheelEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        # Only zoom when Ctrl is pressed
        if modifiers != QtCore.Qt.ControlModifier:
            return

        angle = event.angleDelta().y()

        if angle > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1

        # clamp zoom
        self.zoom_factor = max(self.min_zoom, min(self.zoom_factor, self.max_zoom))

        self.apply_zoom()

    def apply_zoom(self):
        scaled_pixmap = self.original_pixmap.scaled(
            self.original_pixmap.size() * self.zoom_factor,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)
        self.adjustSize()
    
    def copy_to_clipboard(self):
        success = copy_image_to_clipboard(self.image_path)

        if success:
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(),
                "Copied to clipboard"
            )

    def extract_text(self):
        text = extract_text_from_image(self.image_path)

        if not text:
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(),
                "No text found"
            )
            return

        QtWidgets.QApplication.clipboard().setText(text)

        QtWidgets.QToolTip.showText(
            QtGui.QCursor.pos(),
            "Text copied to clipboard"
        )
 
    
