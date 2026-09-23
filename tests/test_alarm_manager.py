import unittest
import datetime
from models import DateTimeAlarm, IntervalAlarm

class TestAlarmModels(unittest.TestCase):
    def test_datetime_alarm_is_due(self):
        now = datetime.datetime.now().astimezone()
        future = now + datetime.timedelta(minutes=1)
        past = now - datetime.timedelta(minutes=1)
        
        # Test future alarm
        alarm = DateTimeAlarm(scheduled_time=future.isoformat())
        self.assertFalse(alarm.is_due(now))
        
        # Test past alarm
        alarm = DateTimeAlarm(scheduled_time=past.isoformat())
        self.assertTrue(alarm.is_due(now))
        
        # Test already triggered
        alarm.triggered = True
        self.assertFalse(alarm.is_due(now))

    def test_interval_alarm_is_due(self):
        now = datetime.datetime.now().astimezone()
        # Set time to 1 minute ago
        past_time = (now - datetime.timedelta(minutes=1)).time()
        
        alarm = IntervalAlarm(time_of_day=past_time.isoformat())
        # Should be due since time has passed today and not triggered
        self.assertTrue(alarm.is_due(now))
        
        # Once triggered today, should not be due
        alarm.last_triggered = now.isoformat()
        self.assertFalse(alarm.is_due(now))
        
        # If triggered yesterday, should be due today
        yesterday = now - datetime.timedelta(days=1)
        alarm.last_triggered = yesterday.isoformat()
        self.assertTrue(alarm.is_due(now))
        
if __name__ == '__main__':
    unittest.main()
