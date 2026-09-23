import os
import sys
import subprocess
from typing import Protocol

class Notifier(Protocol):
    def notify(self, title: str, message: str) -> None:
        ...

class ConsoleNotifier:
    def notify(self, title: str, message: str) -> None:
        print(f"\n--- ALARM: {title} ---\n{message}\n-----------------------\n")


class MacOSNotifier:
    def notify(self, title: str, message: str) -> None:
        # Use osascript to trigger macOS modal alert with sound
        script = f'beep 3\ndisplay alert "{title}" message "{message}" as critical'
        try:
            subprocess.run(['osascript', '-e', script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to send macOS notification: {e}")

def get_notifier() -> Notifier:
    if sys.platform == 'darwin':
        return MacOSNotifier()
    return ConsoleNotifier()
