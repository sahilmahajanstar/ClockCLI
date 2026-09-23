# Python CLI Alarm Clock

A scalable, command-line based alarm clock application written in Python. It supports both one-time date/time alarms and daily interval alarms.

## Flow of Execution (How it works)
1. **User Interaction**: The user uses the CLI commands (like `add`, `toggle`, `delete`) to manage alarms.
2. **Storage**: These CLI commands instantly parse your input and save the alarm details to a local `alarms.json` file.
3. **Background Daemon**: A separate background process (the daemon) runs continuously. It reads the `alarms.json` file to calculate exactly when the next alarm is due.
4. **Dynamic Sleeping**: To save CPU resources, the daemon calculates the precise time until the next alarm and sleeps for that duration (up to a max of 60 seconds, waking up occasionally to check if you added new alarms).
5. **Notification**: Once an alarm's scheduled time is reached, the daemon triggers the `MacOSNotifier` which plays a sound (`beep 3`) and shows a native modal popup alert on the screen that stays until you click "OK".
6. **State Update**: One-time alarms are marked as `triggered: true`, and interval alarms update their `last_triggered` date so they don't fire again until the next day.

<img width="2564" height="1308" alt="image" src="https://github.com/user-attachments/assets/adb4bcc5-ed71-42cd-b298-c5cc836a62a2" />



## Features
- **Date/Time Alarms**: Schedule an alarm for a specific date and time (ISO format).
- **Interval Alarms**: Schedule an alarm to trigger every day at a specific time (HH:MM:SS format).
- **Background Daemon**: A lightweight background process that sleeps dynamically.
- **Native Notifications**: Uses macOS `osascript` to trigger an alert box with sound.
- **Persistent Storage**: Alarms are saved locally in `alarms.json`.

## Setup
Ensure you have Python 3.8+ installed. 

Install the optional dependency (`setproctitle`) so that the background process shows up cleanly as "ClockCliDaemon" in your macOS Activity Monitor:
```bash
pip3 install -r requirements.txt
# (Note: If you use Homebrew Python, you may need to add --break-system-packages)
```

## Usage Commands

### 1. Start the Daemon
To actually monitor the time and trigger alarms, the daemon must be running in the background or in a separate terminal tab:
```bash
python3 cli.py daemon
```

### 2. Add an Alarm
**Date/Time Alarm (One-time):**
```bash
python3 cli.py add --title "Meeting" --type datetime --time 2026-09-23T15:30:00
```
*(Make sure to use ISO format. If no timezone is provided, it uses your system's local time)*

**Interval Alarm (Daily):**
```bash
python3 cli.py add --title "Wake Up" --type interval --time 07:00:00
```
*(Use 24-hour HH:MM:SS format)*

### 3. List Alarms
```bash
python3 cli.py list
```

### 4. Toggle/Disable Alarm
Turn an alarm on or off without deleting it:
```bash
python3 cli.py toggle <alarm_id>
```

### 5. Delete Alarm
```bash
python3 cli.py delete <alarm_id>
```

## Running Tests
To run the automated tests:
```bash
python3 -m unittest discover tests/
```
