import os
import time
from mss import mss
from PIL import Image


def capture_area(rect, save_dir):
    """
    rect: QRect from PyQt
    save_dir: directory to save image
    """

    x = rect.x()
    y = rect.y()
    width = rect.width()
    height = rect.height()

    if width <= 0 or height <= 0:
        return None

    os.makedirs(save_dir, exist_ok=True)

    filename = f"screenshot_{int(time.time())}.png"
    filepath = os.path.join(save_dir, filename)

    with mss() as sct:
        monitor = {
            "left": x,
            "top": y,
            "width": width,
            "height": height
        }

        img = sct.grab(monitor)
        Image.frombytes("RGB", img.size, img.rgb).save(filepath)

    return filepath
