# # app/overlay.py
# from PyQt5.QtWidgets import QWidget, QApplication
# from PyQt5.QtCore import Qt, QRect, pyqtSignal
# from PyQt5.QtGui import QPainter, QColor, QPen


# class ScreenshotOverlay(QWidget):
#     area_selected = pyqtSignal(QRect)

#     def __init__(self):
#         super().__init__()
        

#         # Flags same as your old working overlay
#         self.setWindowFlags(
#             Qt.WindowStaysOnTopHint |
#             Qt.FramelessWindowHint |
#             Qt.Tool
#         )

#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setCursor(Qt.CrossCursor)

#         self.start = None
#         self.end = None
#         self.dragging = False

#         # KEY: use setWindowState + show and force Qt to process events
#         self.setWindowState(Qt.WindowFullScreen)
#         self.show()
#         QApplication.processEvents()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), QColor(0, 0, 0, 150))

#         if self.dragging and self.start and self.end:
#             rect = QRect(self.start, self.end).normalized()

#             painter.setCompositionMode(QPainter.CompositionMode_Clear)
#             painter.fillRect(rect, Qt.transparent)

#             painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
#             painter.setPen(QPen(QColor(0, 120, 215), 2))
#             painter.drawRect(rect)

#     def mousePressEvent(self, event):
#         # Only start on left-button press
#         if event.button() == Qt.LeftButton:
#             self.start = event.pos()
#             self.end = self.start
#             self.dragging = True
#             self.update()

#     def mouseMoveEvent(self, event):
#         if self.dragging:
#             self.end = event.pos()
#             self.update()

#     def mouseReleaseEvent(self, event):
#         if not self.dragging:
#             return
#         # Only respond if left button and a real drag started
#         if event.button() == Qt.LeftButton:
#             self.dragging = False
#             rect = QRect(self.start, self.end).normalized()

#             # Ignore tiny accidental clicks
#             if rect.width() < 5 or rect.height() < 5:
#                 # reset but keep overlay open so user can retry
#                 self.start = None
#                 self.end = None
#                 self.update()
#                 return

#             # hide, let compositor settle, then emit and delete
#             self.hide()
#             QApplication.processEvents()
#             self.area_selected.emit(rect)
#             self.close()

#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Escape:
#             self.close()
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QRect, pyqtSignal


class ScreenshotOverlay(QtWidgets.QWidget):
    area_selected = pyqtSignal(QRect)
    cancelled = pyqtSignal()   # ✅ ADD THIS


    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.activateWindow()
        self.raise_()


        self.start = None
        self.end = None

        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 150))

        if self.start and self.end:
            selection = QtCore.QRect(self.start, self.end).normalized()

            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            painter.fillRect(selection, QtCore.Qt.transparent)

            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 120, 215), 2))
            painter.drawRect(selection)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.start:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.start:
            self.end = event.pos()
            selection = QtCore.QRect(self.start, self.end).normalized()

            self.hide()
            QtWidgets.QApplication.processEvents()

            # 🔑 Emit selection to NEW pipeline
            self.area_selected.emit(selection)

            # 🔑 Let overlay close itself (same as old code)
            QtCore.QTimer.singleShot(200, self.deleteLater)
            
        if selection.width() < 5 or selection.height() < 5:
            self.close()
            return
    

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            QtWidgets.QApplication.processEvents()
            self.cancelled.emit()
            QtCore.QTimer.singleShot(0, self.deleteLater)

