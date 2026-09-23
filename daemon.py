import time
import datetime
from storage import AlarmStorage
from notifier import get_notifier
from models import DateTimeAlarm, IntervalAlarm

class Daemon:
    def __init__(self, storage: AlarmStorage):
        self.storage = storage
        self.notifier = get_notifier()
        
    def _trigger_alarm(self, alarm) -> None:
        self.notifier.notify(alarm.title, f"Alarm Triggered: {alarm.title}")
        
        # Mark as triggered or update last_triggered
        if isinstance(alarm, DateTimeAlarm):
            alarm.triggered = True
            alarm.active = False
        elif isinstance(alarm, IntervalAlarm):
            now_iso = datetime.datetime.now().astimezone().isoformat()
            alarm.last_triggered = now_iso
            
        self.storage.update_alarm(alarm)

    def get_sleep_time(self) -> float:
        alarms = self.storage.get_all()
        now = datetime.datetime.now().astimezone()
        
        min_sleep = 60.0 # Default max sleep is 60 seconds
        
        for alarm in alarms:
            if alarm.is_due(now):
                return 0.0 # Wake up immediately
            next_trigger = alarm.get_next_trigger_time(now)
            if next_trigger:
                diff = (next_trigger - now).total_seconds()
                if 0 < diff < min_sleep:
                    min_sleep = diff
                    
        return min_sleep
        
    def run(self) -> None:
        try:
            import setproctitle
            setproctitle.setproctitle("ClockCliDaemon")
        except ImportError:
            pass
            
        print("Daemon started as 'ClockCliDaemon'. Press Ctrl+C to stop.")
        try:
            while True:
                now = datetime.datetime.now().astimezone()
                alarms = self.storage.get_all()
                
                for alarm in alarms:
                    if alarm.is_due(now):
                        print(f"[{now.isoformat()}] Triggering alarm: {alarm.id} ({alarm.title})")
                        self._trigger_alarm(alarm)
                        
                sleep_time = self.get_sleep_time()
                # Ensure we don't sleep for negative time and at least 0.1s
                sleep_time = max(0.1, sleep_time)
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("\nDaemon stopped.")
