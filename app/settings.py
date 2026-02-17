import os
import json
from PyQt5.QtCore import QStandardPaths


class Settings:
    def __init__(self):
        pictures_dir = QStandardPaths.writableLocation(
            QStandardPaths.PicturesLocation
        )

        screenshots_dir = os.path.join(pictures_dir, "Screenshots")

        self.settings_dir = os.path.join(
            os.getenv("APPDATA"),
            "SmartShot"
        )

        self.settings_path = os.path.join(self.settings_dir, "settings.json")

        self.default_settings = {
            "hotkey": None,
            "save_path": screenshots_dir
        }

        self._ensure_files()
        self.data = self._load()

    def _ensure_files(self):
        os.makedirs(self.settings_dir, exist_ok=True)
        os.makedirs(self.default_settings["save_path"], exist_ok=True)

        if not os.path.exists(self.settings_path):
            with open(self.settings_path, "w") as f:
                json.dump(self.default_settings, f, indent=4)

    def _load(self):
        with open(self.settings_path, "r") as f:
            return json.load(f)

    def get_hotkey(self):
        return self.data.get("hotkey")

    def set_hotkey(self, hotkey_str):
        self.data["hotkey"] = hotkey_str
        with open(self.settings_path, "w") as f:
            json.dump(self.data, f, indent=4)
































# import json
# import os


# class Settings:
#     def __init__(self):
#         self.base_dir = os.path.join(
#             os.getenv("APPDATA"),
#             "SmartShot"
#         )

#         self.settings_path = os.path.join(self.base_dir, "settings.json")

#         self.default_settings = {
#             "hotkey": None,
#             "save_path": os.path.join(self.base_dir, "screenshots")
#         }

#         self._ensure_files()
#         self.data = self._load()

#     def _ensure_files(self):
#         os.makedirs(self.base_dir, exist_ok=True)
#         os.makedirs(self.default_settings["save_path"], exist_ok=True)

#         if not os.path.exists(self.settings_path):
#             with open(self.settings_path, "w") as f:
#                 json.dump(self.default_settings, f, indent=4)

#     def _load(self):
#         with open(self.settings_path, "r") as f:
#             return json.load(f)

#     def get_hotkey(self):
#         return self.data.get("hotkey", self.default_settings["hotkey"])

#     def set_hotkey(self, hotkey_str):
#         self.data["hotkey"] = hotkey_str
#         with open(self.settings_path, "w") as f:
#             json.dump(self.data, f, indent=4)