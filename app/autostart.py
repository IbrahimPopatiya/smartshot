import os
import sys
import win32com.client


def get_startup_folder():
    return os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )


def get_executable_path():
    # If packaged as exe
    if getattr(sys, "frozen", False):
        return sys.executable

    # If running from python
    return sys.argv[0]


def enable_autostart(app_name="SmartShot"):
    startup_dir = get_startup_folder()
    exe_path = get_executable_path()

    shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)

    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = exe_path
    shortcut.save()


def disable_autostart(app_name="SmartShot"):
    shortcut_path = os.path.join(
        get_startup_folder(),
        f"{app_name}.lnk"
    )

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)


def is_autostart_enabled(app_name="SmartShot"):
    shortcut_path = os.path.join(
        get_startup_folder(),
        f"{app_name}.lnk"
    )
    return os.path.exists(shortcut_path)
