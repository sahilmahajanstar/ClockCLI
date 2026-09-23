import uuid
import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class Alarm:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Alarm"
    active: bool = True
    type: str = "base"
    
    def is_due(self, current_time: datetime.datetime) -> bool:
        raise NotImplementedError
        
    def get_next_trigger_time(self, current_time: datetime.datetime) -> Optional[datetime.datetime]:
        raise NotImplementedError

    def to_dict(self) -> dict:
        return asdict(self)
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Alarm':
        alarm_type = data.get("type")
        if alarm_type == "datetime":
            return DateTimeAlarm(**data)
        elif alarm_type == "interval":
            return IntervalAlarm(**data)
        return cls(**data)
        
@dataclass
class DateTimeAlarm(Alarm):
    scheduled_time: str = "" # ISO format string
    type: str = "datetime"
    triggered: bool = False
    
    def is_due(self, current_time: datetime.datetime) -> bool:
        if not self.active or self.triggered:
            return False
        st = datetime.datetime.fromisoformat(self.scheduled_time)
        if st.tzinfo is None:
            st = st.astimezone()
        return current_time >= st

    def get_next_trigger_time(self, current_time: datetime.datetime) -> Optional[datetime.datetime]:
        if not self.active or self.triggered:
            return None
        st = datetime.datetime.fromisoformat(self.scheduled_time)
        if st.tzinfo is None:
            st = st.astimezone()
        if current_time >= st:
            return current_time # Due immediately
        return st
        
@dataclass
class IntervalAlarm(Alarm):
    time_of_day: str = "" # "HH:MM:SS"
    type: str = "interval"
    last_triggered: Optional[str] = None # ISO format string
    
    def is_due(self, current_time: datetime.datetime) -> bool:
        if not self.active:
            return False
            
        t = datetime.time.fromisoformat(self.time_of_day)
        # Create aware datetime for today's trigger
        today_trigger = datetime.datetime.combine(current_time.date(), t, tzinfo=current_time.tzinfo)
        
        if current_time >= today_trigger:
            if not self.last_triggered:
                return True
            last_dt = datetime.datetime.fromisoformat(self.last_triggered)
            if last_dt.date() < current_time.date():
                return True
                
        return False

    def get_next_trigger_time(self, current_time: datetime.datetime) -> Optional[datetime.datetime]:
        if not self.active:
            return None
        
        t = datetime.time.fromisoformat(self.time_of_day)
        today_trigger = datetime.datetime.combine(current_time.date(), t, tzinfo=current_time.tzinfo)
        
        if current_time >= today_trigger:
            if self.last_triggered:
                last_dt = datetime.datetime.fromisoformat(self.last_triggered)
                if last_dt.date() == current_time.date():
                    # Already triggered today, next is tomorrow
                    return today_trigger + datetime.timedelta(days=1)
            # Not triggered yet today and time passed, due now
            return current_time
            
        return today_trigger
