import sys
import os
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.QtGui import QIcon,QFont
from app.clipboard import copy_image_to_clipboard
from app.tray import SystemTray
from app.single_instance import SingleInstance
from app.hotkey import HotkeyListener
from app.settings import Settings
from app.overlay import ScreenshotOverlay
from app.signal_bus import SignalBus
from app.capture import capture_area
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QMetaObject, Qt
from app.floating_preview import FloatingPreview
from app.hotkey_setup import HotkeyCaptureDialog
from app.clipboard import copy_image_to_clipboard
from PyQt5.QtCore import QPoint
from app.autostart import enable_autostart
from app.licensing.license_manager import initialize_trial, is_trial_valid, days_left
from app.licensing.trial_expired_dialog import TrialExpiredDialog


overlay_ref = {"overlay": None}
overlay_active = {"value": False}
floating_refs = []


def main():
    app = QApplication(sys.argv)
    initialize_trial()
    if not is_trial_valid():
        dialog = TrialExpiredDialog()
        result = dialog.exec_()
        print("Trial expired")
        if result == QDialog.Accepted:
            pass
        else:
            sys.exit(0)

    print(f"Trial valid. Days left: {days_left()}")

    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")  # stable & clean on Windows
    app.setFont(QFont("Segoe UI", 9))

    # ---------------- SINGLE INSTANCE ----------------
    APP_KEY = "smartshot_screenshot_tool"
    if SingleInstance.is_running(APP_KEY):
        sys.exit(0)
    instance = SingleInstance(APP_KEY)

    # ---------------- ICON ----------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "assets", "icon.ico")
    app.setWindowIcon(QIcon(icon_path))

    tray = SystemTray(app, icon_path)
    enable_autostart()

    # ---------------- SIGNAL BUS ----------------
    signal_bus = SignalBus()
    overlay_active = {"value": False}

    def show_overlay():
        if overlay_ref["overlay"] is not None:
            return

        print("SCREENSHOT MODE ACTIVATED (Qt main thread)")

        overlay = ScreenshotOverlay()
        overlay_ref["overlay"] = overlay

        def on_area_selected(rect):
            file_path = capture_area(rect, settings.data["save_path"])
            print("📸 Screenshot saved at:", file_path)
            overlay_active["value"] = False
            overlay_ref["overlay"] = None

            if file_path:
                copy_image_to_clipboard(file_path)

                global_pos = overlay.mapToGlobal(rect.topLeft())

                floating = FloatingPreview(image_path=file_path,position=QPoint(global_pos.x(), global_pos.y()))
                floating_refs.append(floating)

                tray.notify("Screenshot saved", "Saved and copied to clipboard")

        def on_destroyed():
            overlay_active["value"] = False
            overlay_ref["overlay"] = None

        overlay.area_selected.connect(on_area_selected)

        def on_cancel():
            overlay_active["value"] = False
            overlay_ref["overlay"] = None
            print("Screenshot cancelled")

        overlay.cancelled.connect(on_cancel)
        overlay.destroyed.connect(on_destroyed)


        
        
    signal_bus.show_overlay.connect(show_overlay)


    # ---------------- SETTINGS ----------------
    settings = Settings()
    hotkey = settings.get_hotkey()

    if not hotkey:
        dialog = HotkeyCaptureDialog()
        if dialog.exec_() == dialog.Accepted and dialog.hotkey:
            settings.set_hotkey(dialog.hotkey)
            hotkey = dialog.hotkey
            print("Hotkey set to:", hotkey)
        else:
            print("Hotkey setup cancelled. Exiting.")
            sys.exit(0)


    # ---------------- HOTKEY LISTENER ----------------
    def on_hotkey_pressed():
        if overlay_active["value"]:
            return

        overlay_active["value"] = True
        print("SCREENSHOT MODE REQUESTED (background thread)")

        # 🔑 Safely schedule overlay in Qt main thread
        QMetaObject.invokeMethod(
            signal_bus,
            "show_overlay",
            Qt.QueuedConnection
        )


    hotkey_listener = HotkeyListener(hotkey, on_hotkey_pressed)
    hotkey_listener.start()

    
    def check_hotkey_listener():
        if not hotkey_listener.is_alive():
            print("Hotkey listener stopped. Restarting...")
            hotkey_listener.start()

    watchdog_timer = QTimer()
    watchdog_timer.timeout.connect(check_hotkey_listener)
    watchdog_timer.start(3000)  # check every 3 seconds


    def on_app_state_changed(state):

        if state == Qt.ApplicationActive:
            print("App resumed. Re-registering hotkey...")

            # Force restart hotkey listener
            hotkey_listener.stop()
            hotkey_listener.start()

    app.applicationStateChanged.connect(on_app_state_changed)
    # ---------------- EVENT LOOP ----------------
    sys.exit(app.exec_())



