from pynput import keyboard
import threading
import time

KEY_MAP = {
    "ctrl": keyboard.Key.ctrl_l,
    "shift": keyboard.Key.shift,
    "alt": keyboard.Key.alt_l,
    "cmd": keyboard.Key.cmd,
}


class HotkeyListener:
    def __init__(self, hotkey_str, on_trigger):
        self.on_trigger = on_trigger
        self.hotkey_str = hotkey_str.lower()

        self.hotkey = self._parse_hotkey(hotkey_str)
        self.current_keys = set()

        self.listener = None
        self.thread = None
        self.running = False

        

    def _parse_hotkey(self, hotkey_str):
        keys = set()

        for part in hotkey_str.split("+"):
            part = part.strip()

            if part in KEY_MAP:
                keys.add(KEY_MAP[part])
            else:
                keys.add(keyboard.KeyCode.from_char(part))

        return keys

    def start(self):
        if self.running:
            return

        self.running = True
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )
        self.thread.start()

    def _run(self):
        try:
            self.listener.start()
            self.listener.join()
        except Exception as e:
            print("Hotkey listener crashed:", e)
        finally:
            self.running = False

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.running = False

    def is_alive(self):
        return self.running and self.thread and self.thread.is_alive()

    def on_press(self, key):
        if key in self.hotkey:
            self.current_keys.add(key)

        if self.hotkey.issubset(self.current_keys):
            if not getattr(self, "_triggered", False):
                self._triggered = True
                self.on_trigger()

    def on_release(self, key):
        self.current_keys.discard(key)
        if key in self.hotkey:
            self._triggered = False