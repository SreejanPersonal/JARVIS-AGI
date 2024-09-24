from typing import List, Dict, Tuple, Any
from win10toast import ToastNotifier
import datetime
import threading
import json
import os

class AlarmManager:
    """
    Manages the scheduling, storing, and triggering of alarms and timers.
    """

    def __init__(self, verbose: bool = False) -> None:
        """
        Initializes the AlarmManager with a notifier and loads existing alarms.

        Args:
            verbose (bool, optional): Whether to print status messages. Defaults to False.
        """
        self._notifier: ToastNotifier = ToastNotifier()
        self._alarm_file: str = 'ASSETS/alarms.json'
        self._verbose: bool = verbose
        self._alarms: List[Dict[str, str]] = self._load_alarms()

    def _load_alarms(self) -> List[Dict[str, str]]:
        """
        Loads alarms from the JSON file. Handles the case where the file
        is empty to prevent JSONDecodeError.

        Returns:
            List[Dict[str, str]]: A list of alarm dictionaries,
                                  where each dictionary has the keys 'time' (str)
                                  representing the alarm time in '%Y-%m-%d %H:%M:%S' format
                                  and 'type' (str) representing the type of alarm
                                  ('alarm' or 'timer'). Returns an empty list if the
                                  file is empty.
        """
        if os.path.exists(self._alarm_file):
            with open(self._alarm_file, 'r') as f:
                try:
                    data = json.load(f)
                    return data
                except json.JSONDecodeError:  # Handle empty file
                    return []
        return []

    def _save_alarms(self) -> None:
        """
        Saves the current alarms to the JSON file.
        """
        with open(self._alarm_file, 'w') as f:
            json.dump(self._alarms, f)

    def _is_duplicate_alarm(self, alarm_time: str, alarm_type: str) -> bool:
        """
        Checks if an alarm with the same time and type already exists.

        Args:
            alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
            alarm_type (str): The type of alarm ('alarm' or 'timer').

        Returns:
            bool: True if duplicate, False otherwise.
        """
        for alarm in self._alarms:
            if alarm['time'] == alarm_time and alarm['type'] == alarm_type:
                return True
        return False

    def _add_alarm(self, alarm_time: str, alarm_type: str) -> None:
        """
        Adds a new alarm to the list and saves it.

        Args:
            alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
            alarm_type (str): The type of alarm ('alarm' or 'timer').
        """
        self._alarms.append({'time': alarm_time, 'type': alarm_type})
        self._save_alarms()
        if self._verbose:
            print(f"\033[92mAdded {alarm_type} for {alarm_time}\033[0m")

    def _remove_alarm(self, alarm_time: str) -> None:
        """
        Removes an alarm from the list and saves the updated list.

        Args:
            alarm_time (str): The time of the alarm to remove in '%Y-%m-%d %H:%M:%S' format.
        """
        self._alarms = [alarm for alarm in self._alarms if alarm['time'] != alarm_time]
        self._save_alarms()
        if self._verbose:
            print(f"\033[93mRemoved alarm for {alarm_time}\033[0m")

    def _check_and_ring_alarm(self, alarm_time: str, alarm_type: str) -> None:
        """
        Checks if an alarm should ring now or schedules it for later.

        Args:
            alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
            alarm_type (str): The type of alarm ('alarm' or 'timer').
        """
        now = datetime.datetime.now()
        alarm_datetime = datetime.datetime.strptime(alarm_time, '%Y-%m-%d %H:%M:%S')

        if alarm_datetime > now:
            time_diff = (alarm_datetime - now).total_seconds()
            threading.Timer(time_diff, self._ring_alarm, args=[alarm_time, alarm_type]).start()
        else:
            if self._verbose:
                print(f"\033[91mMissed alarm for {alarm_time}\033[0m")
            self._remove_alarm(alarm_time)

    def _ring_alarm(self, alarm_time: str, alarm_type: str) -> None:
        """
        Triggers the alarm notification and removes it from the list.

        Args:
            alarm_time (str): The time of the alarm in '%Y-%m-%d %H:%M:%S' format.
            alarm_type (str): The type of alarm ('alarm' or 'timer').
        """
        if self._verbose:
            print(f"\033[94m{alarm_type.capitalize()} ringing for {alarm_time}\033[0m")
        self._notifier.show_toast("DevsDoCode's JARVIS", f"{alarm_type.capitalize()} For " + alarm_time + "", duration=5)
        self._remove_alarm(alarm_time)

    def schedule_all_alarms(self) -> None:
        """
        Schedules all loaded alarms.
        """
        for alarm in self._alarms:
            self._check_and_ring_alarm(alarm['time'], alarm['type'])

    def set_alarm(self, hour: int, minute: int, meridiem: str, date: str = None) -> Dict[str, str]:
        """
        Sets a new alarm.

        Args:
            hour (int): The hour of the alarm (12-hour format).
            minute (int): The minute of the alarm.
            meridiem (str): 'AM' or 'PM'.
            date (str, optional): The date in '%Y-%m-%d' format (defaults to today).

        Returns:
            Dict[str, str]: A dictionary containing the status ('success' or 'error')
                            and a message.
        """
        return self.set_alarm_or_timer(hour, minute, meridiem, date, 'alarm')

    def set_timer(self, hours: int, minutes: int) -> Dict[str, str]:
        """
        Sets a new timer.

        Args:
            hours (int): The number of hours for the timer.
            minutes (int): The number of minutes for the timer.

        Returns:
            Dict[str, str]: A dictionary containing the status ('success' or 'error')
                            and a message.
        """
        now = datetime.datetime.now()
        if hours is None: hours = 0
        if minutes is None: minutes = 0
        alarm_time = (now + datetime.timedelta(hours=hours, minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')

        if self._is_duplicate_alarm(alarm_time, 'timer'):
            return {'status': 'error', 'message': f'Timer for {alarm_time} is already set.'}

        self._add_alarm(alarm_time, 'timer')
        self._check_and_ring_alarm(alarm_time, 'timer')
        return {'status': 'success', 'message': f'Timer for {alarm_time} has been set.'}

    def set_alarm_or_timer(self, hour: int, minute: int, meridiem: str, date: str = None, alarm_type: str = 'alarm') -> Dict[str, str]:
        """
        Sets a new alarm or timer.

        Args:
            hour (int): The hour of the alarm (12-hour format).
            minute (int): The minute of the alarm.
            meridiem (str): 'AM' or 'PM'.
            date (str, optional): The date in '%Y-%m-%d' format (defaults to today).
            alarm_type (str, optional): 'alarm' or 'timer'. Defaults to 'alarm'.

        Returns:
            Dict[str, str]: A dictionary containing the status ('success' or 'error')
                            and a message.
        """
        if self._verbose:
            print(f"\033[96mSetting {alarm_type} for {hour}:{minute} {meridiem} on {date}\033[0m")

        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        if hour is None: hour = 0
        if meridiem.upper() == 'PM' and hour < 12:
            hour += 12
        elif meridiem.upper() == 'AM' and hour == 12:
            hour = 0
        alarm_time = f'{date} {hour:02d}:{minute:02d}:00'

        if self._is_duplicate_alarm(alarm_time, alarm_type):
            try: return {'status': 'error', 'message': f'{alarm_type.capitalize()} for {alarm_time} is already set.'}
            except: return {'status': 'error', 'message': f'{alarm_time} is already set.'}

        self._add_alarm(alarm_time, alarm_type)
        self._check_and_ring_alarm(alarm_time, alarm_type)
        try: return {'status': 'success', 'message': f'{alarm_type.capitalize()} for {alarm_time} has been set.'}
        except: return {'status': 'success', 'message': f'{alarm_time} has been set.'}

if __name__ == "__main__":
    alarm_manager = AlarmManager(verbose=True)
    alarm_manager.schedule_all_alarms()

    now = datetime.datetime.now()
    print(alarm_manager.set_alarm(now.hour, now.minute + 1, 'PM'))
    print(alarm_manager.set_timer(0, 1))



"***********************************************************************************************************"

"""AlarmManager is a class that manages the scheduling, storing, and triggering of alarms and timers. Deprecated v1.0.0"""

"***********************************************************************************************************"


# from typing import List, Dict, Tuple, Any
# from win10toast import ToastNotifier
# import datetime
# import threading
# import json
# import os

# class AlarmManager:
#     """
#     Manages the scheduling, storing, and triggering of alarms and timers.
#     """

#     def __init__(self, verbose: bool = False) -> None:
#         """
#         Initializes the AlarmManager with a notifier and loads existing alarms.

#         Args:
#             verbose (bool, optional): Whether to print status messages. Defaults to False.
#         """
#         self._notifier: ToastNotifier = ToastNotifier()
#         self._alarm_file: str = 'ASSETS/alarms.json'
#         self._verbose: bool = verbose
#         self._alarms: List[Dict[str, str]] = self._load_alarms()

#     def _load_alarms(self) -> List[Dict[str, str]]:
#         """
#         Loads alarms from the JSON file. Handles the case where the file 
#         is empty to prevent JSONDecodeError.

#         Returns:
#             List[Dict[str, str]]: A list of alarm dictionaries, 
#                                   where each dictionary has the keys 'time' (str) 
#                                   representing the alarm time in '%Y-%m-%d %H:%M:%S' format 
#                                   and 'type' (str) representing the type of alarm 
#                                   ('alarm' or 'timer'). Returns an empty list if the
#                                   file is empty.
#         """
#         if os.path.exists(self._alarm_file):
#             with open(self._alarm_file, 'r') as f:
#                 try:
#                     data = json.load(f)
#                     return data 
#                 except json.JSONDecodeError:  # Handle empty file
#                     return []
#         return []
    
#     def _save_alarms(self) -> None:
#         """
#         Saves the current alarms to the JSON file.
#         """
#         with open(self._alarm_file, 'w') as f:
#             json.dump(self._alarms, f)

#     def _is_duplicate_alarm(self, alarm_time: str, alarm_type: str) -> bool:
#         """
#         Checks if an alarm with the same time and type already exists.

#         Args:
#             alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
#             alarm_type (str): The type of alarm ('alarm' or 'timer').

#         Returns:
#             bool: True if duplicate, False otherwise.
#         """
#         for alarm in self._alarms:
#             if alarm['time'] == alarm_time and alarm['type'] == alarm_type:
#                 return True
#         return False

#     def _add_alarm(self, alarm_time: str, alarm_type: str) -> None:
#         """
#         Adds a new alarm to the list and saves it.

#         Args:
#             alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
#             alarm_type (str): The type of alarm ('alarm' or 'timer').
#         """
#         self._alarms.append({'time': alarm_time, 'type': alarm_type})
#         self._save_alarms()
#         if self._verbose:
#             print(f"\033[92mAdded {alarm_type} for {alarm_time}\033[0m")

#     def _remove_alarm(self, alarm_time: str) -> None:
#         """
#         Removes an alarm from the list and saves the updated list.

#         Args:
#             alarm_time (str): The time of the alarm to remove in '%Y-%m-%d %H:%M:%S' format.
#         """
#         self._alarms = [alarm for alarm in self._alarms if alarm['time'] != alarm_time]
#         self._save_alarms()
#         if self._verbose:
#             print(f"\033[93mRemoved alarm for {alarm_time}\033[0m")

#     def _check_and_ring_alarm(self, alarm_time: str, alarm_type: str) -> None:
#         """
#         Checks if an alarm should ring now or schedules it for later.

#         Args:
#             alarm_time (str): The alarm time in '%Y-%m-%d %H:%M:%S' format.
#             alarm_type (str): The type of alarm ('alarm' or 'timer').
#         """
#         now = datetime.datetime.now()
#         alarm_datetime = datetime.datetime.strptime(alarm_time, '%Y-%m-%d %H:%M:%S')

#         if alarm_datetime > now:
#             time_diff = (alarm_datetime - now).total_seconds()
#             threading.Timer(time_diff, self._ring_alarm, args=[alarm_time, alarm_type]).start()
#         else:
#             if self._verbose:
#                 print(f"\033[91mMissed alarm for {alarm_time}\033[0m")
#             self._remove_alarm(alarm_time)

#     def _ring_alarm(self, alarm_time: str, alarm_type: str) -> None:
#         """
#         Triggers the alarm notification and removes it from the list.

#         Args:
#             alarm_time (str): The time of the alarm in '%Y-%m-%d %H:%M:%S' format.
#             alarm_type (str): The type of alarm ('alarm' or 'timer').
#         """
#         if self._verbose:
#             print(f"\033[94m{alarm_type.capitalize()} ringing for {alarm_time}\033[0m")
#         self._notifier.show_toast("DevsDoCode's JARVIS", f"{alarm_type.capitalize()} For " + alarm_time + "", duration=5)
#         self._remove_alarm(alarm_time)

#     def schedule_all_alarms(self) -> None:
#         """
#         Schedules all loaded alarms.
#         """
#         for alarm in self._alarms:
#             self._check_and_ring_alarm(alarm['time'], alarm['type'])

#     def set_alarm_or_timer(self, hour: int, minute: int, meridiem: str, date: str = None, alarm_type: str = 'alarm') -> Dict[str, str]:
#         """
#         Sets a new alarm or timer.

#         Args:
#             hour (int): The hour of the alarm (12-hour format).
#             minute (int): The minute of the alarm.
#             meridiem (str): 'AM' or 'PM'.
#             date (str, optional): The date in '%Y-%m-%d' format (defaults to today).
#             alarm_type (str, optional): 'alarm' or 'timer'. Defaults to 'alarm'.

#         Returns:
#             Dict[str, str]: A dictionary containing the status ('success' or 'error') 
#                             and a message.
#         """
#         if self._verbose:
#             print(f"\033[96mSetting {alarm_type} for {hour}:{minute} {meridiem} on {date}\033[0m")

#         if date is None:
#             date = datetime.datetime.now().strftime('%Y-%m-%d')
#         if meridiem.upper() == 'PM' and hour < 12:
#             hour += 12
#         elif meridiem.upper() == 'AM' and hour == 12:
#             hour = 0
#         alarm_time = f'{date} {hour:02d}:{minute:02d}:00'

#         if self._is_duplicate_alarm(alarm_time, alarm_type):
#             return {'status': 'error', 'message': f'{alarm_type.capitalize()} for {alarm_time} is already set.'}

#         self._add_alarm(alarm_time, alarm_type)
#         self._check_and_ring_alarm(alarm_time, alarm_type)
#         return {'status': 'success', 'message': f'{alarm_type.capitalize()} for {alarm_time} has been set.'}

# if __name__ == "__main__":
#     alarm_manager = AlarmManager(verbose=True)
#     alarm_manager.schedule_all_alarms()

#     now = datetime.datetime.now()
#     print(alarm_manager.set_alarm_or_timer(now.hour, now.minute + 1, 'PM'))
#     print(alarm_manager.set_alarm_or_timer(now.hour, now.minute + 2, 'AM', alarm_type='timer'))
#     print(alarm_manager.set_alarm_or_timer(23, 12, 'AM', alarm_type='timer'))


    # import time
    # while True:
    #     print("Working In Thread...")
    #     time.sleep(2)



"***********************************************"

"""Random Function. Not Working Code. Need to fix"""

"***********************************************"


# import os
# import sys
# from datetime import datetime
# import winsound

# def play_alarm_sound():
#     try:
#         # Play the system default sound
#         winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
#         print("Alarm sounded successfully.")
#     except Exception as e:
#         print(f"Failed to play sound: {e}")

# def schedule_alarm(task_name, alarm_time):
#     # Calculate the time difference from now to the alarm time
#     now = datetime.now()
#     alarm_datetime = datetime.strptime(alarm_time, "%Y-%m-%d %H:%M:%S")
    
#     if alarm_datetime <= now:
#         raise ValueError("Alarm time must be in the future")

#     time_str = alarm_datetime.strftime("%H:%M")
#     date_str = alarm_datetime.strftime("%d/%m/%Y")  # Correct date format for schtasks

#     # Command to create a scheduled task
#     python_executable = sys.executable
#     script_path = os.path.abspath(__file__)
#     command = f'schtasks /create /tn "{task_name}" /tr "{python_executable} {script_path} --play-sound" /sc once /st {time_str} /sd {date_str} /f'
    
#     # Execute the command
#     os.system(command)

# if __name__ == "__main__":
#     if "--play-sound" in sys.argv:
#         play_alarm_sound()
#     else:
#         try:
#             task_name = "WakeUpAlarm"
#             alarm_time = "2024-06-20 09:43:00"  # Replace with the desired alarm time
#             schedule_alarm(task_name, alarm_time)
#             print("Alarm set successfully!")
#         except ValueError as e:
#             print(e)