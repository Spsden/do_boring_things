import json
import time
import threading
from pynput import mouse, keyboard


class EventLogger:
    def __init__(self, log_file="logs\events_log.json"):
        self.log_file = log_file
        self.logging_active = False
        self.mouse_listener = None
        self.keyboard_listener = None

    def log_event(self, event_data):
        try:
            with open(self.log_file, "a") as file:
                file.write(json.dumps(event_data) + "\n")
        except Exception as e:
            print(f"Error writing log: {e}")

    def on_mouse_click(self, x, y, button, pressed):
        if self.logging_active:
            event = {
                "timestamp": time.time(),
                "event": "mouse_click",
                "button": str(button),
                "position": (x, y),
                "pressed": pressed
            }
            self.log_event(event)

    def on_mouse_move(self, x, y):
        if self.logging_active:
            event = {
                "timestamp": time.time(),
                "event": "mouse_move",
                "position": (x, y)
            }
            self.log_event(event)

    def on_key_press(self, key):
        if self.logging_active:
            try:
                key_str = key.char if hasattr(key, 'char') else str(key)
                event = {
                    "timestamp": time.time(),
                    "event": "key_press",
                    "key": key_str
                }
                self.log_event(event)
            except Exception as e:
                print(f"Error logging key: {e}")

    def start_logging(self):
        if self.logging_active:
            print("⚠️ Logger already running!")
            return

        self.logging_active = True
        print("🟢 Event logging started...")

        # Create listener threads
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click, on_move=self.on_mouse_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

        # Run in separate thread to avoid blocking
        threading.Thread(target=self._wait_for_stop, daemon=True).start()

    def stop_logging(self):
        """Stops event logging."""
        if not self.logging_active:
            return

        self.logging_active = False
        print("🔴 Event logging stopped!")

        # Stop listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def _wait_for_stop(self):
        try:
            self.mouse_listener.join()
            self.keyboard_listener.join()
        except Exception as e:
            print(f"⚠️ Logger thread error: {e}")
