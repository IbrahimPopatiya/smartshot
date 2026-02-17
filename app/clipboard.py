from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage
import os


def copy_image_to_clipboard(image_path: str):
    if not os.path.exists(image_path):
        return False

    image = QImage(image_path)
    if image.isNull():
        return False

    QApplication.clipboard().setImage(image)
    return True
