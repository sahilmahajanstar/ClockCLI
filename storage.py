import json
import os
from typing import List, Optional
from models import Alarm

class AlarmStorage:
    def __init__(self, file_path: str = "alarms.json"):
        self.file_path = file_path
        
    def _load_raw(self) -> List[dict]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
            
    def _save_raw(self, data: List[dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    def get_all(self) -> List[Alarm]:
        raw_data = self._load_raw()
        alarms = []
        for item in raw_data:
            try:
                alarms.append(Alarm.from_dict(item))
            except Exception:
                pass # Skip invalid alarms
        return alarms
        
    def save_all(self, alarms: List[Alarm]) -> None:
        raw_data = [a.to_dict() for a in alarms]
        self._save_raw(raw_data)
        
    def get_alarm(self, alarm_id: str) -> Optional[Alarm]:
        for alarm in self.get_all():
            if alarm.id == alarm_id:
                return alarm
        return None
        
    def add_alarm(self, alarm: Alarm) -> None:
        alarms = self.get_all()
        alarms.append(alarm)
        self.save_all(alarms)
        
    def update_alarm(self, updated_alarm: Alarm) -> bool:
        alarms = self.get_all()
        for i, alarm in enumerate(alarms):
            if alarm.id == updated_alarm.id:
                alarms[i] = updated_alarm
                self.save_all(alarms)
                return True
        return False
        
    def delete_alarm(self, alarm_id: str) -> bool:
        alarms = self.get_all()
        initial_count = len(alarms)
        alarms = [a for a in alarms if a.id != alarm_id]
        if len(alarms) < initial_count:
            self.save_all(alarms)
            return True
        return False
