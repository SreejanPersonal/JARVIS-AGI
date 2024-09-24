from TOOLS.TimeComponents import extract_time_components
from TOOLS.TimeComponents_mod import extract_time_components_mod
from TOOLS.SYSTEM_SETTINGS import Alarms
from ENGINE.STT import DevsDoCode
from ENGINE.TTS import edge_tts

if __name__ == "__main__":
    listener = DevsDoCode.SpeechToTextListener(language="en-IN")  # You can specify the desired language here
    alarm_manager = Alarms.AlarmManager(verbose=True)

    while True: 
        speech = listener.listen()
        print("FINAL EXTRACTION: ", speech)
        # hour, minute, am_pm, date, alarm_timer = extract_time_components(speech)
        hour, minute, am_pm, date, alarm_timer = extract_time_components_mod(speech)
        print(f"Hour: {hour}, Minute: {minute}, AM/PM: {am_pm}, Date: {date}, Alarm/Timer: {alarm_timer}")
        if alarm_timer == 'alarm':
            resposne = alarm_manager.set_alarm(hour, minute, am_pm, date)
        elif alarm_timer == 'timer':
            resposne = alarm_manager.set_timer(hour, minute)
        # resposne = alarm_manager.set_alarm_or_timer(hour, minute, am_pm, date, alarm_timer)
        print("Response Status: ", resposne['status'], "Response Message: ", resposne['message'])
        edge_tts.speak(resposne['message'])