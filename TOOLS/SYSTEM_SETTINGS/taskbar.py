import winreg
from typing import Optional

class TaskbarCustomizer:
    """A utility class to customize the appearance of the Windows taskbar.

    This class provides methods to modify the alignment of the taskbar 
    (left or center) and to enable or disable the display of the 
    temperature within the taskbar.
    """

    def __init__(self, alignment: Optional[int] = None, use_temperature: Optional[int] = None) -> None:
        """Initializes the TaskbarCustomizer object.

        Note: Currently, the `alignment` and `use_temperature` parameters
        are not used during initialization. They are included for 
        potential future enhancements where default settings could be applied 
        directly upon object creation.

        Args:
            alignment (int, optional): Future parameter to set initial taskbar alignment 
                                        (1 for center, 0 for left). Defaults to None.
            use_temperature (int, optional): Future parameter to set initial temperature 
                                        display state (1 for enabled, 0 for disabled). 
                                        Defaults to None.
        """
        self.alignment = alignment
        self.use_temperature = use_temperature
        self.REGISTRY_KEY_PATH: str = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"

    def _set_registry_value(self, value_name: str, data: int) -> None:
        """Sets a DWORD value in the taskbar's registry key.

        This is an internal helper method that provides a centralized way to 
        modify DWORD values within the Windows registry related to the taskbar.

        Args:
            value_name (str): The name of the registry value to modify.
            data (int): The integer value to set for the specified registry value.

        Raises:
            winreg.error: If there's an error accessing or writing to the registry.
        """
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                self.REGISTRY_KEY_PATH, 
                0, 
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, data)
                print(f"Successfully set '{value_name}' to {data}.")
        except winreg.error as e:
            print(f"Error writing to registry: {e}")

    def set_alignment(self, alignment: int) -> None:
        """Sets the horizontal alignment of the taskbar.

        Args:
            alignment (int): 1 to center the taskbar, 0 to align it to the left.

        Raises:
            TypeError: If the provided `alignment` is not an integer.
            ValueError: If the provided `alignment` is not 0 or 1.
        """
        if not isinstance(alignment, int):
            raise TypeError("Alignment value must be an integer (0 or 1).")
        if alignment not in (0, 1):
            raise ValueError("Invalid alignment value. Use 0 for left or 1 for center.")
        
        self._set_registry_value("TaskbarAl", alignment)

    def set_temperature_display(self, use_temperature: int) -> None:
        """Controls the display of the temperature on the taskbar.

        Args:
            use_temperature (int): 1 to enable the temperature display, 0 to disable it.

        Raises:
            TypeError: If the provided `use_temperature` is not an integer.
            ValueError: If the provided `use_temperature` is not 0 or 1.
        """
        if not isinstance(use_temperature, int):
            raise TypeError("Use temperature value must be an integer (0 or 1).")
        if use_temperature not in (0, 1):
            raise ValueError("Invalid temperature display value. Use 0 to disable or 1 to enable.")
        
        self._set_registry_value("TaskbarDa", use_temperature)


if __name__ == "__main__":
    customizer = TaskbarCustomizer()

    while True:
        try:
            alignment_input = int(
                input("Enter 1 to align taskbar to center, 0 for left (or any other key to skip): ")
            )
            customizer.set_alignment(alignment_input)
        except ValueError:
            pass  

        try:
            temperature_input = int(
                input("Enter 1 to enable taskbar temperature, 0 to disable (or any other key to skip): ")
            )
            customizer.set_temperature_display(temperature_input) 
        except ValueError:
            pass 