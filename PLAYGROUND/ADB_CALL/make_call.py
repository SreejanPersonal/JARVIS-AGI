import subprocess

def call(number: str = "7272733232", isd_code: str = "+91") -> str:
    """
    Initiates a phone call to the specified number using the ADB command.

    Parameters:
    - number (str): The phone number to call. Defaults to your NUMBER
    - isd_code (str): The ISD (International Subscriber Dialing) code. Defaults to "+91".

    Returns:
    - str: A message indicating the status of the call initiation process.
    """

    command = "adb.exe shell am start -a android.intent.action.CALL -d tel:{}{}".format(isd_code, number)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("Successfully Called the Number {}".format(number))
    # Store the terminal response in variables
    terminal_output = result.stdout
    terminal_error = result.stderr

    if terminal_error != None: return "Disconnect the device from USB. More than one device connected."
    else: "Success"

if __name__ == "__main__":
    import android_device_connection_setup
    import time
    android_device_connection_setup.initialise()
    time.sleep(2)
    call("9999999999")