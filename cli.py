import argparse
import datetime
from storage import AlarmStorage
from models import DateTimeAlarm, IntervalAlarm
from daemon import Daemon

def parse_args():
    parser = argparse.ArgumentParser(description="Python CLI Alarm Clock")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Add alarm
    parser_add = subparsers.add_parser("add", help="Add a new alarm")
    parser_add.add_argument("--title", required=True, help="Title or message for the alarm")
    parser_add.add_argument("--type", choices=["datetime", "interval"], required=True, help="Type of alarm")
    parser_add.add_argument("--time", required=True, help="Scheduled time. For datetime: ISO format (e.g. 2026-09-23T10:00:00). For interval: HH:MM:SS")
    
    # List alarms
    parser_list = subparsers.add_parser("list", help="List all alarms")
    
    # Delete alarm
    parser_del = subparsers.add_parser("delete", help="Delete an alarm")
    parser_del.add_argument("id", help="ID of the alarm to delete")
    
    # Toggle active status
    parser_toggle = subparsers.add_parser("toggle", help="Toggle alarm active status")
    parser_toggle.add_argument("id", help="ID of the alarm to toggle")
    
    # Start daemon
    parser_daemon = subparsers.add_parser("daemon", help="Start the background alarm daemon")
    
    return parser.parse_args()

def main():
    args = parse_args()
    storage = AlarmStorage()
    
    if args.command == "add":
        if args.type == "datetime":
            try:
                # Validate iso format
                datetime.datetime.fromisoformat(args.time)
                alarm = DateTimeAlarm(title=args.title, scheduled_time=args.time)
            except ValueError:
                print("Error: Invalid datetime format. Please use ISO format, e.g., 2026-09-23T10:00:00+05:30")
                return
        elif args.type == "interval":
            try:
                # Validate time format
                datetime.time.fromisoformat(args.time)
                alarm = IntervalAlarm(title=args.title, time_of_day=args.time)
            except ValueError:
                print("Error: Invalid time format. Please use HH:MM:SS, e.g., 10:00:00")
                return
                
        storage.add_alarm(alarm)
        print(f"Added alarm '{alarm.title}' with ID: {alarm.id}")
        
    elif args.command == "list":
        alarms = storage.get_all()
        if not alarms:
            print("No alarms found.")
        for a in alarms:
            status = "Active" if a.active else "Inactive"
            print(f"[{status}] ID: {a.id} | Title: {a.title} | Type: {a.type}")
            if a.type == "datetime":
                print(f"  -> Scheduled for: {a.scheduled_time}")
                print(f"  -> Triggered: {a.triggered}")
            elif a.type == "interval":
                print(f"  -> Time of day: {a.time_of_day}")
                print(f"  -> Last triggered: {a.last_triggered}")
            print("-" * 40)
            
    elif args.command == "delete":
        if storage.delete_alarm(args.id):
            print(f"Deleted alarm {args.id}")
        else:
            print(f"Alarm {args.id} not found")
            
    elif args.command == "toggle":
        alarm = storage.get_alarm(args.id)
        if alarm:
            alarm.active = not alarm.active
            storage.update_alarm(alarm)
            print(f"Alarm {args.id} is now {'Active' if alarm.active else 'Inactive'}")
        else:
            print(f"Alarm {args.id} not found")
            
    elif args.command == "daemon":
        daemon = Daemon(storage)
        daemon.run()

if __name__ == "__main__":
    main()
