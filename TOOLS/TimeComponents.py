import re
import datetime
from typing import Tuple, Optional

def extract_date_component(input_text: str) -> datetime.date:
    """
    Extracts date information from a text string.

    Args:
        input_text: The input text string.

    Returns:
        The date extracted from the text or the current date if no date is specified.
    """
    normalized_text = input_text.lower()

    # Check for specific keywords
    if "tomorrow" in normalized_text:
        return datetime.date.today() + datetime.timedelta(days=1)
    elif "yesterday" in normalized_text:
        return datetime.date.today() - datetime.timedelta(days=1)

    # Check for weekday names
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for weekday in weekdays:
        if weekday in normalized_text:
            today = datetime.date.today()
            weekday_index = weekdays.index(weekday)
            today_index = today.weekday()
            days_until_weekday = (weekday_index - today_index) % 7
            return today + datetime.timedelta(days=days_until_weekday)

    # If no date is specified, return the current date
    return datetime.date.today()

def extract_time_components(input_text: str) -> Tuple[Optional[int], Optional[int], Optional[str], datetime.date, Optional[str]]:
    """
    Extracts hour, minute, AM/PM, date and alarm/timer information from a text string.

    Args:
        input_text: The input text string.

    Returns:
        A tuple containing:
            - hour (int or None)
            - minute (int or None)
            - am_pm (str: 'am', 'pm', or None if not specified)
            - date (datetime.date)
            - alarm_timer (str: 'alarm', 'timer', or None if not specified)
    """
    normalized_text = input_text.lower()
    alarm_timer = None
    
    if 'alarm' in normalized_text:
        alarm_timer = 'alarm'
    elif 'timer' in normalized_text:
        alarm_timer = 'timer'

    # Match patterns like "5:30", "10.15", "23.45", "14:30" (no am/pm)
    time_match = re.search(r'(\d{1,2})[:.](\d{2})', normalized_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        am_pm = determine_am_pm(hour, normalized_text)
        date = extract_date_component(input_text)
        return hour, minute, am_pm, date, alarm_timer

    # Match patterns like "5 pm", "6 am", "ten thirty pm", "eight o'clock"
    # (Excluding cases with colons - ":")
    time_match = re.search(r'((?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)(?:\s+(?:thirty|fifteen))?)\s+(a\.?m\.?|p\.?m\.?|o\'clock)', normalized_text)
    if time_match:
        time_part = time_match.group(1)
        am_pm = time_match.group(2)

        if am_pm == "o'clock":
            am_pm = determine_am_pm(convert_word_to_number(time_part.split()[0]), normalized_text)
        else:
            am_pm = 'am' if am_pm.startswith('a') else 'pm'

        if " " in time_part:
            hour, minute_word = time_part.split()
            hour = convert_word_to_number(hour)
            minute = convert_word_to_number(minute_word)
        else:
            hour = convert_word_to_number(time_part)
            minute = 0

        date = extract_date_component(input_text)
        return hour, minute, am_pm, date, alarm_timer

    # Match patterns like "1 hour 2 minutes", "2 hours 15 minutes"
    time_match = re.search(r'((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty)\s*hour(?:s)?)\s*((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty)\s*minute(?:s)?)?', normalized_text)
    if time_match:
        hour_part = time_match.group(1)
        minute_part = time_match.group(2)
        hour = int(re.search(r'\d+', hour_part).group(0)) if re.search(r'\d+', hour_part) else convert_word_to_number(hour_part)
        minute = int(re.search(r'\d+', minute_part).group(0)) if minute_part and re.search(r'\d+', minute_part) else convert_word_to_number(minute_part) if minute_part else 0
        date = extract_date_component(input_text)
        return hour, minute, None, date, alarm_timer

    # Match patterns like "20 minutes", "five minutes timer"
    time_match = re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty)\s*minutes?\s*(?:timer)?', normalized_text)
    if time_match:
        minute_part = time_match.group(1)
        minute = int(minute_part) if minute_part.isdigit() else convert_word_to_number(minute_part)
        date = extract_date_component(input_text)
        return None, minute, None, date, alarm_timer

    # Match patterns like "1 hour", "in 1 hour"
    time_match = re.search(r'(?:in|\s)(\d+|one)\s*hour(?:s)?', normalized_text)
    if time_match:
        hour_part = time_match.group(1)
        hour = int(hour_part) if hour_part.isdigit() else convert_word_to_number(hour_part)
        date = extract_date_component(input_text)
        return hour, None, None, date, alarm_timer

    # Match patterns like "half past 5", "quarter to 6"
    time_match = re.search(r'(half|quarter)\s*(past|to)\s*(\d{1,2})', normalized_text)
    if time_match:
        modifier = time_match.group(1)
        relation = time_match.group(2)
        hour = int(time_match.group(3))

        minute = 30 if modifier == 'half' else 15

        if relation == 'to':
            hour = (hour - 1) % 12  # Use modulo to handle 12-hour wrap-around
            if hour == 0:
                hour = 12
            minute = 60 - minute

        am_pm = determine_am_pm(hour, normalized_text)  # Determine AM/PM after hour adjustment
        date = extract_date_component(input_text)
        return hour, minute, am_pm, date, alarm_timer

    # Match patterns like "one hour and twenty minutes"
    time_match = re.search(r'((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty)\s*hour(?:s)?)\s*and\s*((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty)\s*minutes?)', normalized_text)
    if time_match:
        hour_part = time_match.group(1)
        minute_part = time_match.group(2)
        hour = int(re.search(r'\d+', hour_part).group(0)) if re.search(r'\d+', hour_part) else convert_word_to_number(hour_part)
        minute = int(re.search(r'\d+', minute_part).group(0)) if re.search(r'\d+', minute_part) else convert_word_to_number(minute_part)
        am_pm = determine_am_pm(hour, normalized_text)
        date = extract_date_component(input_text)
        return hour, minute, am_pm, date, alarm_timer

    date = extract_date_component(input_text)
    return None, None, None, date, alarm_timer

def convert_word_to_number(word: str) -> int:
    """
    Converts a number word to its numerical equivalent.
    """
    word_to_number_map = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'twenty-one': 21, 'twenty-two': 22,
        'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25,
        'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28,
        'twenty-nine': 29, 'thirty': 30, 'thirty-one': 31,
        'thirty-two': 32, 'thirty-three': 33, 'thirty-four': 34,
        'thirty-five': 35, 'thirty-six': 36, 'thirty-seven': 37,
        'thirty-eight': 38, 'thirty-nine': 39, 'forty': 40,
        'forty-one': 41, 'forty-two': 42, 'forty-three': 43,
        'forty-four': 44, 'forty-five': 45, 'forty-six': 46,
        'forty-seven': 47, 'forty-eight': 48, 'forty-nine': 49,
        'fifty': 50, 'fifty-one': 51, 'fifty-two': 52, 'fifty-three': 53,
        'fifty-four': 54, 'fifty-five': 55, 'fifty-six': 56,
        'fifty-seven': 57, 'fifty-eight': 58, 'fifty-nine': 59,
        'sixty': 60
    }
    return word_to_number_map.get(word)

def determine_am_pm(hour: int, text: str) -> str:
    """
    Determines AM/PM based on the hour value and the original text.
    """
    am_match = re.search(r'\b(a\.?m\.?)\b', text, re.IGNORECASE)
    pm_match = re.search(r'\b(p\.?m\.?)\b', text, re.IGNORECASE)
    
    if am_match:
        return 'am'
    elif pm_match:
        return 'pm'
    elif 0 <= hour <= 11:
        return 'am'
    elif 12 <= hour <= 23:
        return 'pm'
    else:
        return None  # Handle invalid hour values

if __name__ == '__main__':
    test_cases = [
        "Set an alarm for 5:30 p.m. tomorrow",
        "Wake me up at 6 am on Wednesday",
        "Set a timer for 20 minutes",
        "Reminder at 10.15 am today",
        "Set an alarm for ten thirty pm",
        "five minutes timer",
        "Remind me in one hour and twenty minutes",
        "set alarm in 1 hour",
        "Set an alarm for half past 5",
        "Wake me up at quarter to 6 pm",
        "Reminder at 14:30",
        "Set a timer for 30 minutes",
        "Set an alarm for 23.45",
        "Set alarm at eight o'clock tomorrow",
        "Wake me up at nine am on Friday",
        "Set a reminder for 12:00",
        "Set an alarm for 0:00",
        "Set alarm for quarter to eleven pm",
        "Set alarm for half past one am",
        "Set alarm for ten thirty pm",
        "Set a reminder for nine fifteen am",
        "Set alarm for five o'clock",
        "set a timer for 1 hour 2 minute",
        "Set an alarm for 7:00 a.m.",
        "Reminder at 3:45 p.m."
    ]

    for text in test_cases:
        hour, minute, am_pm, date, alarm_timer = extract_time_components(text)
        print(f"\033[34mText: '{text}'\033[0m -> \033[31mHour: {hour}\033[0m, \033[32mMinute: {minute}\033[0m, \033[33mAM/PM: {am_pm}\033[0m, \033[35mDate: {date}\033[0m, \033[36mAlarm/Timer: {alarm_timer}\033[0m")