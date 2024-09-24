import re
import datetime
import calendar
from typing import Tuple, Optional
from dateutil.parser import parse

def extract_date_component(input_text: str) -> Tuple[datetime.date, str]:
    """Extracts the date component from the input text.

    Parses the input text to identify and extract date-related information, such as 'tomorrow', 'yesterday',
    specific weekdays, or specific dates. Removes the identified date phrases from the text.

    Args:
        input_text (str): The text input containing potential date information.

    Returns:
        Tuple[datetime.date, str]: A tuple containing the extracted date and the remaining text with date
        information removed.
    """
    normalized_input = input_text.lower()
    today = datetime.date.today()
    remaining_text = normalized_input

    if "tomorrow" in normalized_input:
        remaining_text = re.sub(r'\btomorrow\b', '', remaining_text)
        return today + datetime.timedelta(days=1), remaining_text
    elif "yesterday" in normalized_input:
        remaining_text = re.sub(r'\byesterday\b', '', remaining_text)
        return today - datetime.timedelta(days=1), remaining_text

    weekdays = ["monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday"]

    for weekday in weekdays:
        weekday_pattern = r'\b(?:next\s+)?' + weekday + r'\b'
        match = re.search(weekday_pattern, normalized_input)
        if match:
            weekday_index = weekdays.index(weekday)
            today_index = today.weekday()
            days_until_weekday = (weekday_index - today_index) % 7
            if f'next {weekday}' in normalized_input:
                days_until_weekday += 7
            elif days_until_weekday == 0:
                days_until_weekday = 7
            remaining_text = re.sub(weekday_pattern, '', remaining_text)
            return today + datetime.timedelta(days=days_until_weekday), remaining_text

    if "next week" in normalized_input:
        remaining_text = re.sub(r'\bnext week\b', '', remaining_text)
        return today + datetime.timedelta(weeks=1), remaining_text
    elif "end of the month" in normalized_input:
        remaining_text = re.sub(r'\bend of the month\b', '', remaining_text)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        return last_day, remaining_text

    # Match formats like 'May 5th', '5th May', 'the 3rd of July'
    date_match = re.search(
        r'(?:(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(january|february|march|april|may|june|july|august|'
        r'september|october|november|december)|'
        r'(?:on\s+)?(january|february|march|april|may|june|july|august|'
        r'september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?)', normalized_input)
    if date_match:
        year = today.year
        if date_match.group(1):
            day = int(date_match.group(1))
            month = date_match.group(2)
        else:
            day = int(date_match.group(4))
            month = date_match.group(3)
        try:
            date = datetime.date(year, list(calendar.month_name).index(month.capitalize()), day)
            matched_text = date_match.group(0)
            remaining_text = normalized_input.replace(matched_text, '')
            return date, remaining_text
        except ValueError:
            pass

    try:
        dt, tokens = parse(input_text, fuzzy_with_tokens=True)
        date = dt.date()
        tokens = [token for token in tokens if not re.search(r'\d', token)]
        remaining_text = ' '.join(tokens).lower()
        return date, remaining_text
    except ValueError:
        return today, normalized_input

def extract_time_components_mod(input_text: str) -> Tuple[Optional[int], Optional[int], Optional[str], datetime.date, Optional[str]]:
    """Extracts the time components and additional details from the input text.

    Parses the input text to identify time information, including hours, minutes, AM/PM indicators, along with
    the date and whether the text pertains to an alarm, timer, or reminder. Handles various formats of time
    expressions.

    Args:
        input_text (str): The text input containing potential time and date information.

    Returns:
        Tuple[Optional[int], Optional[int], Optional[str], datetime.date, Optional[str]]: A tuple containing
        the hour, minute, AM/PM indicator, date, and type of alarm, timer, or reminder.
    """

    # Define number words and regex patterns locally
    NUMBER_WORDS_LIST = [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty',
        'forty', 'fifty', 'sixty'
    ]
    NUMBER_WORDS_REGEX = '|'.join(NUMBER_WORDS_LIST)
    WORD_TO_NUMBER_MAP = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'half': 30, 'quarter': 15
    }

    date, remaining_text = extract_date_component(input_text)

    if 'alarm' in remaining_text:
        alarm_timer = 'alarm'
    elif 'timer' in remaining_text:
        alarm_timer = 'timer'
    elif 'reminder' in remaining_text or 'remind me' in remaining_text:
        alarm_timer = 'reminder'
    else:
        alarm_timer = None

    remaining_text = remaining_text.lower()
    remaining_text = re.sub(r'\b(\d+)(st|nd|rd|th)\b', r'\1', remaining_text)

    # First, check for durations (timers or 'in X minutes/hours')
    if alarm_timer == 'timer' or 'in ' in remaining_text or 'from now' in remaining_text:
        duration_patterns = [
            r'(?:in\s+)?(?P<hour>\d+|' + NUMBER_WORDS_REGEX + r')\s*hours?\s*(?:and\s*)?'
            r'(?P<minute>\d+|' + NUMBER_WORDS_REGEX + r')?\s*minutes?',
            r'(?:in\s+)?(?P<minute>\d+|' + NUMBER_WORDS_REGEX + r')\s*minutes?',
            r'(?:in\s+)?(?P<hour>\d+|' + NUMBER_WORDS_REGEX + r')\s*hours?',
        ]
        for pattern in duration_patterns:
            time_match = re.search(pattern, remaining_text)
            if time_match:
                hour = None
                minute = None
                if time_match.groupdict().get('hour'):
                    hour_part = time_match.group('hour')
                    hour = convert_word_to_number(hour_part)
                else:
                    hour = 0
                if time_match.groupdict().get('minute'):
                    minute_part = time_match.group('minute')
                    minute = convert_word_to_number(minute_part)
                else:
                    minute = 0
                return hour, minute, None, date, alarm_timer

    # Next, check for times like '14:30' or '2:30 pm'
    time_match = re.search(r'(\d{1,2})[:\.](\d{2})(?:\s*(a\.?m\.?|p\.?m\.?))?', remaining_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        am_pm = time_match.group(3)
        if am_pm:
            am_pm = 'am' if 'a' in am_pm else 'pm'
        else:
            am_pm = determine_am_pm(hour, remaining_text)
        return hour, minute, am_pm, date, alarm_timer

    # Then, check for phrases like 'half past', 'quarter to', etc.
    time_match = re.search(
        r'\b(half|quarter)\s*(past|to)\s*(' + NUMBER_WORDS_REGEX + r'|\d{1,2})\s*(a\.?m\.?|p\.?m\.?)?',
        remaining_text)
    if time_match:
        modifier = time_match.group(1)
        relation = time_match.group(2)
        hour = convert_word_to_number(time_match.group(3))
        am_pm = time_match.group(4)
        if am_pm:
            am_pm = 'am' if 'a' in am_pm else 'pm'
        minute = WORD_TO_NUMBER_MAP[modifier]
        if relation == 'to':
            hour = (hour - 1) % 12 or 12
            minute = 60 - minute
        if not am_pm:
            am_pm = determine_am_pm(hour, remaining_text)
        return hour, minute, am_pm, date, alarm_timer

    # Then, check for time expressed in words like 'ten thirty pm'
    time_match = re.search(
        r'\b(at\s+)?(' + NUMBER_WORDS_REGEX + r'|\d{1,2})\s+(' + NUMBER_WORDS_REGEX + r'|\d{1,2})\s*(a\.?m\.?|p\.?m\.?|o\'clock)?',
        remaining_text)
    if time_match:
        hour_part = time_match.group(2)
        minute_part = time_match.group(3)
        hour = convert_word_to_number(hour_part)
        minute = convert_word_to_number(minute_part)
        am_pm = time_match.group(4)
        if am_pm == "o'clock":
            am_pm = determine_am_pm(hour, remaining_text)
        elif am_pm:
            am_pm = 'am' if 'a' in am_pm else 'pm'
        else:
            am_pm = determine_am_pm(hour, remaining_text)
        return hour, minute, am_pm, date, alarm_timer

    # Then, check for time expressed in 'X o'clock'
    time_match = re.search(
        r'\b(at\s+)?(' + NUMBER_WORDS_REGEX + r'|\d{1,2})\s*(o\'?clock)?\s*(a\.?m\.?|p\.?m\.?)?',
        remaining_text)
    if time_match:
        hour_part = time_match.group(2)
        hour = convert_word_to_number(hour_part)
        minute = 0
        am_pm = time_match.group(4) if time_match.group(4) else time_match.group(3)
        if am_pm == "o'clock" or not am_pm:
            am_pm = determine_am_pm(hour, remaining_text)
        else:
            am_pm = 'am' if 'a' in am_pm else 'pm'
        return hour, minute, am_pm, date, alarm_timer

    # If all else fails, try to parse using dateutil
    try:
        datetime_parsed = parse(input_text, fuzzy=True)
        hour = datetime_parsed.hour
        minute = datetime_parsed.minute
        am_pm = 'am' if hour < 12 else 'pm'
        date = datetime_parsed.date()
        return hour, minute, am_pm, date, alarm_timer
    except Exception:
        pass

    # If no time is found, default to current time
    return None, None, None, date, alarm_timer

def convert_word_to_number(word: str) -> int:
    """Converts a number expressed in words to its numeric value.

    Handles numbers that may be written as words (e.g., 'twenty-one') or digits, and converts them to integers.
    Also handles compound numbers like 'twenty one'.

    Args:
        word (str): The word representing the number.

    Returns:
        int: The numeric value of the word.
    """
    WORD_TO_NUMBER_MAP = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
        'fifty': 50, 'sixty': 60, 'half': 30, 'quarter': 15
    }
    word = word.lower()
    if word.isdigit():
        return int(word)
    elif word in WORD_TO_NUMBER_MAP:
        return WORD_TO_NUMBER_MAP[word]
    else:
        words = word.replace('-', ' ').split()
        total = 0
        for w in words:
            if w in WORD_TO_NUMBER_MAP:
                total += WORD_TO_NUMBER_MAP[w]
        return total

def determine_am_pm(hour: int, text: str) -> str:
    """Determines whether the time is AM or PM based on the hour and text.

    Checks for explicit AM/PM indicators in the text; if absent, infers AM/PM based on the hour.

    Args:
        hour (int): The hour component of the time.
        text (str): The original text input.

    Returns:
        str: 'am' or 'pm' indicating the time period.
    """
    am_match = re.search(r'\b(a\.?m\.?)\b', text, re.IGNORECASE)
    pm_match = re.search(r'\b(p\.?m\.?)\b', text, re.IGNORECASE)

    if am_match:
        return 'am'
    elif pm_match:
        return 'pm'
    else:
        return 'am' if hour < 12 else 'pm'

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
        "Reminder at 3:45 p.m.",
        "Set an alarm for 5:05 pm",
        "Remind me in 30 minutes",
        "Set a timer for 2 hours from now",
        "Set an alarm for next Monday at 3pm",
        "Reminder on May 5th at 2pm",
        "Set an alarm for the 3rd of July at 9am"
    ]

    for text in test_cases:
        try:
            hour, minute, am_pm, date, alarm_timer = extract_time_components_mod(text)
            print(f"\033[34mInput Text: '{text}'\033[0m -> \033[31mHour: {hour}\033[0m, "
                  f"\033[32mMinute: {minute}\033[0m, \033[33mAM/PM: {am_pm}\033[0m, "
                  f"\033[35mDate: {date}\033[0m, \033[36mType: {alarm_timer}\033[0m")
        except Exception as e:
            print(f"\033[31mError processing: '{text}'\033[0m")
            print(f"\033[31mError message: {str(e)}\033[0m")