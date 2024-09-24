import winreg
from typing import Literal

class WindowsThemeManager:
    """
    Provides a streamlined interface for managing Windows theme settings
    through direct interaction with the Windows Registry.

    Attributes:
        key_path (str): The registry key path for theme personalization settings. 
                         Defaults to "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize".

    Example:
        >>> manager = WindowsThemeManager()
        >>> manager.set_theme(0)  # Set dark mode
        >>> manager.set_theme(1)  # Set light mode
    """
    ThemeMode = Literal[0, 1]  # Define a custom type for theme modes

    def __init__(self, key_path: str = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"):
        """Initializes the WindowsThemeManager with the registry key path."""
        self.key_path = key_path

    def _set_registry_value(self, key_name: str, dword_value: int, verbose: bool = False) -> None:
        """
        Sets a DWORD (double-word) value for a specific key within the Windows Registry.

        Args:
            key_name (str): The name of the registry key to modify.
            dword_value (int): The DWORD value to set.
            verbose (bool, optional): If True, prints a confirmation message upon success. 
                                       Defaults to False.

        Raises:
            winreg.error: If an error occurs during registry access or modification. 
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, dword_value)
            if verbose: 
                print(f"Registry value '{key_name}' set successfully.")
        except winreg.error as e:
            raise winreg.error(f"Error setting registry value: {e}") from e 

    def set_theme(self, theme_mode: ThemeMode) -> None:
        """
        Simultaneously sets both application and system-wide themes to either 
        light or dark mode by modifying the corresponding registry entries.

        Args:
            theme_mode (ThemeMode): 0 for dark mode, 1 for light mode.

        Raises:
            ValueError: If an invalid theme_mode is provided. 
        """
        if theme_mode not in [0, 1]:
            raise ValueError("Invalid theme_mode. Use 0 for dark mode or 1 for light mode.")

        self._set_registry_value("AppsUseLightTheme", theme_mode)
        self._set_registry_value("SystemUseLightTheme", theme_mode)

if __name__ == "__main__":
    manager = WindowsThemeManager()

    while True:
        try:
            user_input = int(input("Enter 0 for dark mode or 1 for light mode: "))
            manager.set_theme(user_input)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")