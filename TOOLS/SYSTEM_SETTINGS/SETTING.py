"""
[System Theme]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize\SystemUsesLightTheme (DWORD: 0 = Dark, 1 = Light)

[App Theme]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize\AppsUseLightTheme (DWORD: 0 = Dark, 1 = Light)

[Accent Color]
Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\DWM\ColorPrevalence (DWORD: 0 = Off, 1 = On)
Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\DWM\AccentColor (DWORD: Color value in hexadecimal)

[Desktop Background]
Computer\HKEY_CURRENT_USER\Control Panel\Desktop\WallPaper (String: Path to image file)

[Screen Resolution] 
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Configuration\{Your Display Adapter ID}\00\00\DisplayModes\CurrentMode (Various values for width, height, refresh rate, etc.) 
# Note: Finding your display adapter ID can be tricky. Consider adjusting screen resolution through Windows settings instead.

[Disable Lock Screen]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Personalization\NoLockScreen (DWORD: 1 = Disabled)

[Show Hidden Files and Folders]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Hidden (DWORD: 1 = Show, 2 = Hide)

[Enable/Disable Hibernation]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power\HibernateEnabled (DWORD: 1 = Enabled, 0 = Disabled)

[Startup Programs (Current User)]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run (Add/remove string values with the path to the program executable)

[Startup Programs (All Users)]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run (Add/remove string values with the path to the program executable)

[Enable/Disable Network Discovery]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\{Network Profile GUID}\Category (DWORD: 1 = Private, 2 = Public. Search for your network's GUID.)

[Change Default Sharing Settings] 
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\HomeGroup\Sharing (Various values for different sharing options)

[Always Show File Extensions]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\HideFileExt (DWORD: 0 = Show, 1 = Hide)

[Disable File Explorer's Quick Access]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DisableStartData (DWORD: 1 = Disable)

[Show Full Path in Title Bar]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\ShowFullPathInTitleBar (DWORD: 1 = Enabled, 0 = Disabled)

[Disable File Explorer's Advertising (Upsell) Notifications]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DisableNotificationCenter (DWORD: 1 = Disable)

[Disable Aero Shake (Window minimizing)]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\DisallowShaking (DWORD: 1 = Disable)

[Disable Aero Peek (Desktop preview on taskbar hover)]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\DisablePreviewDesktop (DWORD: 1 = Disable)

[Change Menu Show Delay]
Computer\HKEY_CURRENT_USER\Control Panel\Desktop\MenuShowDelay (String: Delay in milliseconds - e.g., "400")

[Enable/Disable Transparency Effects]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\DWM\TransparencyEnabled (DWORD: 1 = Enabled, 0 = Disabled)

[Disable UAC (User Account Control) Prompts] 
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA (DWORD: 0 = Disable. WARNING: NOT RECOMMENDED - significantly lowers security)

[Configure Windows Defender (Antivirus) Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender (Various values for real-time protection, exclusions, and more) 
# Note: Use extreme caution when modifying antivirus settings.

[Change Time Synchronization Server]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters\NtpServer (String:  The address of the new time server)

[Disable Automatic Driver Updates]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\DriverSearching\SearchOrderConfig (DWORD: 0 = Disable. May require additional settings changes.)

[Taskbar Size (Small or Large)]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarSi (DWORD: 0 = Small, 1 = Large)

[Hide Labels on Taskbar Buttons]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarGlomLevel (DWORD: 2 = Hide labels)

[Move Taskbar (Top, Left, Right)]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3 (Binary Value: This one's more involved. Edit the binary data to change taskbar position. Research carefully before attempting.)

[Combine Taskbar Buttons]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarGlomLevel (DWORD: 0 = Always Combine, 1 = Combine when full, 2 = Never Combine)

[Disable Recently Added Apps in Start Menu]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Explorer\Settings\DisableRegistryTools (DWORD: 1 = Disabled) 

[Disable "Most Used" List in Start Menu]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Start_TrackProgs (DWORD: 0 = Disabled)

[Remove Default Apps from Start Menu] 
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultApplications (Delete the specific key for the app you want to remove) 
# WARNING: Be extremely careful deleting keys here!

[Disable Window Animations]
Computer\HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics\MinAnimate (DWORD: 0 = Disabled, 1 = Enabled)

[Change Mouse Cursor Scheme]
Computer\HKEY_CURRENT_USER\Control Panel\Cursors (String values: You can change the cursor files used for different system actions.)

[Customize Font Smoothing]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes (String values: Allows for advanced font rendering customizations and substitutions. Proceed with caution!)

[Always Show Full Ribbon in File Explorer]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Ribbon\AlwaysShowCmdBar (DWORD: 1 = Enabled)

[Disable Automatic Updates] 
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU (DWORD: 0 = Disable Automatic Updates)

[Disable Windows Update Notifications]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\NoAutoUpdate (DWORD: 1 = Disable Notifications)

[Change Default Browser] 
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice (String: Path to the desired browser's executable)

[Change Default Mail Client]
Computer\HKEY_CLASSES_ROOT\mailto\shell\open\command (String: Path to the desired mail client's executable)

[Change Default Media Player]
Computer\HKEY_CLASSES_ROOT\*\shell\open\command (String: Path to the desired media player's executable)

[Change Default Photo Viewer]
Computer\HKEY_CLASSES_ROOT\jpegfile\shell\open\command (String: Path to the desired photo viewer's executable)

[Change Default Text Editor]
Computer\HKEY_CLASSES_ROOT\txtfile\shell\open\command (String: Path to the desired text editor's executable)

[Change Default Archive Program]
Computer\HKEY_CLASSES_ROOT\zipfile\shell\open\command (String: Path to the desired archive program's executable)

[Change Default PDF Viewer]
Computer\HKEY_CLASSES_ROOT\PDFFile\shell\open\command (String: Path to the desired PDF viewer's executable)

[Change Default Video Player]
Computer\HKEY_CLASSES_ROOT\aviFile\shell\open\command (String: Path to the desired video player's executable)

[Change Default Audio Player]
Computer\HKEY_CLASSES_ROOT\mp3file\shell\open\command (String: Path to the desired audio player's executable)

[Change Default File Association]
Computer\HKEY_CLASSES_ROOT\ (Find the specific file extension you want to modify and change the associated application)

[Disable Cortana]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Windows Search\AllowCortana (DWORD: 0 = Disable Cortana)

[Disable Windows Search Indexing]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Search (DWORD: 0 = Disable Indexing)

[Disable Windows Defender Real-time Protection]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection (DWORD: 0 = Disable)

[Disable Windows Defender Scheduled Scans]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Scan (DWORD: 0 = Disable)

[Disable Windows Defender Firewall]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\WindowsFirewall\StandardProfile\EnableFirewall (DWORD: 0 = Disable)

[Disable Windows Defender SmartScreen]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Windows Defender\SmartScreenEnabled (DWORD: 0 = Disable)

[Disable Windows Defender Exploit Guard]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\ExploitGuard (DWORD: 0 = Disable)

[Disable Windows Defender Tamper Protection]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\TamperProtection (DWORD: 0 = Disable)

[Disable Windows Update for Business]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU (DWORD: 0 = Disable)

[Disable Windows Update for Education]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU (DWORD: 0 = Disable)

[Change Windows Update Delivery Optimization Settings] 
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\DeliveryOptimization (Various DWORD values for different settings)

[Disable Windows Hello]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System\AllowSignInOptions (DWORD: 0 = Disable Windows Hello)

[Disable Windows Ink Workspace]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\PenAndTouch\AllowInkWorkspace (DWORD: 0 = Disable)

[Disable Windows Narrator]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowNarrator (DWORD: 0 = Disable)

[Disable Windows Magnifier]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowMagnifier (DWORD: 0 = Disable)

[Disable Windows On-Screen Keyboard]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowOnScreenKeyboard (DWORD: 0 = Disable)

[Change Mouse Click Speed] 
Computer\HKEY_CURRENT_USER\Control Panel\Mouse\MouseSpeed (DWORD: Value 1-20, higher value = faster click speed)

[Change Mouse Double-Click Speed]
Computer\HKEY_CURRENT_USER\Control Panel\Mouse\DoubleClickSpeed (DWORD: Value 1-20, higher value = faster double-click speed)

[Change Mouse Scroll Speed]
Computer\HKEY_CURRENT_USER\Control Panel\Mouse\MouseWheelScrollLines (DWORD: Value 1-20, higher value = faster scroll speed)

[Change Mouse Pointer Size]
Computer\HKEY_CURRENT_USER\Control Panel\Mouse\MouseSensitivity (DWORD: Value 1-20, higher value = larger pointer size)

[Change Mouse Pointer Color] 
Computer\HKEY_CURRENT_USER\Control Panel\Mouse\MousePointerColor (DWORD: Value 0-16, higher value = different color)

[Change Keyboard Repeat Rate]
Computer\HKEY_CURRENT_USER\Control Panel\Keyboard\KeyboardSpeed (DWORD: Value 1-31, higher value = faster repeat rate)

[Change Keyboard Repeat Delay]
Computer\HKEY_CURRENT_USER\Control Panel\Keyboard\KeyboardDelay (DWORD: Value 1-31, higher value = longer delay before repeating)

[Change Keyboard Cursor Blink Rate]
Computer\HKEY_CURRENT_USER\Control Panel\Keyboard\CursorBlinkRate (DWORD: Value 1-20, higher value = faster blink rate)

[Change Keyboard Cursor Size]
Computer\HKEY_CURRENT_USER\Control Panel\Keyboard\CursorSize (DWORD: Value 1-20, higher value = larger cursor size)

[Change Keyboard Layout]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts (String: Add/modify layouts)

[Disable Windows Hello Face Recognition]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System\AllowFaceAuthentication (DWORD: 0 = Disable)

[Disable Windows Subsystem for Linux]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WSL\Disabled (DWORD: 1 = Disable)

[Change Windows Update Active Hours]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU\SetActiveHours (DWORD: 1-24, sets active hours)

[Disable Windows Update Restart Warning]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU\NoAutoRestart (DWORD: 1 = Disable warning)

[Change Windows Defender Cloud-Delivered Protection]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\CloudDeliveredProtection (DWORD: 1 = Enable)

[Disable Windows Defender Advanced Threat Protection]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\AdvancedThreatProtection (DWORD: 0 = Disable)

[Change Windows Search Bar Behavior]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\SearchBar (DWORD: 1 = Enable, 0 = Disable)

[Disable Windows Ink Workspace Button]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\PenAndTouch\AllowInkWorkspaceButton (DWORD: 0 = Disable)

[Change Windows Narrator Voices]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Accessibility\Narrator\V2\Voice (String: Path to voice file)

[Disable Windows Magnifier Zoom]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowMagnifierZoom (DWORD: 0 = Disable)

[Change Windows On-Screen Keyboard Layout]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Accessibility\OnScreenKeyboard\Layout (String: Path to layout file)

[Disable Windows Touch Keyboard]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowTouchKeyboard (DWORD: 0 = Disable)

[Change Windows Sticky Keys Behavior]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\StickyKeys (DWORD: 1 = Enable, 0 = Disable)

[Disable Windows Filter Keys]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowFilterKeys (DWORD: 0 = Disable)

[Change Windows Toggle Keys]
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\ToggleKeys (DWORD: 1 = Enable, 0 = Disable)

[Disable Windows Sound Sentences]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Accessibility\AllowSoundSentences (DWORD: 0 = Disable)

[Change Windows Display Adapters]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E968-E325-11CE-BFC1-08002BE10318} (String: Adapter settings)

[Disable Windows Audio Enhancements]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Audio\AudioEnhancements (DWORD: 0 = Disable)

[Change Windows Audio Effects]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Audio\AudioEffects (String: Effect settings)

[Disable Windows Audio Playback]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Audio\Playback (DWORD: 0 = Disable)

[Change Windows Audio Recording]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Audio\Recording (String: Recording settings)

[Disable Windows Audio Inputs]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Audio\Inputs (DWORD: 0 = Disable)

[Change Windows Power Settings]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power (String: Power settings)

[Disable Windows Hibernation Timeout]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Power\HibernateTimeout (DWORD: 0 = Disable)

[Change Windows Lid Close Action]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\LidCloseAction (String: Action setting)

[Disable Windows Sleep Button]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Power\SleepButton (DWORD: 0 = Disable)

[Change Windows Power Button Action]
Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\PowerButtonAction (String: Action setting)

[Disable Windows Wake Timers]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Power\WakeTimers (DWORD: 0 = Disable)

[Disable Windows Subsystem for Android]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WSA\Disabled (DWORD: 1 = Disable)

[Change Windows Camera Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Camera (String: Camera settings)

[Disable Windows PrintFax]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\PrintFax\Disabled (DWORD: 1 = Disable)

[Change Windows Fax Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Fax (String: Fax settings)

[Disable Windows Phone]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Phone\Disabled (DWORD: 1 = Disable)

[Change Windows Phone Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Phone (String: Phone settings)

[Disable Windows Messaging]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Messaging\Disabled (DWORD: 1 = Disable)

[Change Windows Messaging Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Messaging (String: Messaging settings)

[Disable Windows Appointment Reminders]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\AppointmentReminders\Disabled (DWORD: 1 = Disable)

[Change Windows Reminders Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Reminders (String: Reminders settings)

[Disable Windows Maps]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Maps\Disabled (DWORD: 1 = Disable)

[Change Windows Maps Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Maps (String: Maps settings)

[Disable Windows Alarms & Clock]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\AlarmsAndClock\Disabled (DWORD: 1 = Disable)

[Change Windows Alarms & Clock Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AlarmsAndClock (String: Alarms & Clock settings)

[Disable Windows Photos]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Photos\Disabled (DWORD: 1 = Disable)

[Change Windows Photos Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Photos (String: Photos settings)

[Disable Windows Voice Recorder]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\VoiceRecorder\Disabled (DWORD: 1 = Disable)

[Change Windows Voice Recorder Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\VoiceRecorder (String: Voice Recorder settings)

[Disable Windows Scan]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Scan\Disabled (DWORD: 1 = Disable)

[Change Windows Scan Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Scan (String: Scan settings)

[Disable Windows People]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\People\Disabled (DWORD: 1 = Disable)

[Change Windows People Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\People (String: People settings)

[Disable Windows Calendar]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Calendar\Disabled (DWORD: 1 = Disable)

[Change Windows Calendar Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Calendar (String: Calendar settings)

[Disable Windows Mail]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Mail\Disabled (DWORD: 1 = Disable)

[Change Windows Mail Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Mail (String: Mail settings)

[Disable Windows Feedback]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Feedback\Disabled (DWORD: 1 = Disable)

[Change Windows Feedback Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Feedback (String: Feedback settings)

[Disable Windows Tips]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Tips\Disabled (DWORD: 1 = Disable)

[Change Windows Tips Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Tips (String: Tips settings)

[Disable Windows Game Bar]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\GameBar (DWORD: 0 = Disable)

[Change Windows Game DVR Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR (String: DVR settings)

[Disable Windows Game Streaming]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\GameStreaming\Disabled (DWORD: 1 = Disable)

[Change Windows Game Streaming Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\GameStreaming (String: Streaming settings)

[Disable Windows Xbox App]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\XboxApp\Disabled (DWORD: 1 = Disable)

[Change Windows XBOX App Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\XboxApp (String: Xbox App settings)

[Disable Windows Microsoft Store]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\MicrosoftStore\Disabled (DWORD: 1 = Disable)

[Change Windows Microsoft Store Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\MicrosoftStore (String: Microsoft Store settings)

[Disable Windows Microsoft Edge]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\MicrosoftEdge\Disabled (DWORD: 1 = Disable)

[Change Windows Microsoft Edge Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\MicrosoftEdge (String: Microsoft Edge settings)

[Disable Windows Microsoft Teams]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\MicrosofTeams\Disabled (DWORD: 1 = Disable)

[Change Windows Microsoft Teams Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\MicrosofTeams (String: Microsoft Teams settings)

[Disable Windows Office]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Office\Disabled (DWORD: 1 = Disable)

[Change Windows Office Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Office (String: Office settings)

[Disable Windows OneDrive]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\OneDrive\Disabled (DWORD: 1 = Disable)

[Change Windows OneDrive Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\OneDrive (String: OneDrive settings)

[Disable Windows Outlook]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Outlook\Disabled (DWORD: 1 = Disable)

[Change Windows Outlook Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Outlook (String: Outlook settings)

[Disable Windows Paint 3D]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Paint3D\Disabled (DWORD: 1 = Disable)

[Change Windows Paint 3D Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Paint3D (String: Paint 3D settings)

[Disable Windows Remote Desktop]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\RemoteDesktop\Disabled (DWORD: 1 = Disable)

[Change Windows Remote Desktop Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RemoteDesktop (String: Remote Desktop settings)

[Disable Windows Remote Assistance]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\RemoteAssistance\Disabled (DWORD: 1 = Disable)

[Change Windows Remote Assistance Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RemoteAssistance (String: Remote Assistance settings)

[Disable Windows SharePoint Workspace]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\SharePointWorkspace\Disabled (DWORD: 1 = Disable)

[Change Windows SharePoint Workspace Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\SharePointWorkspace (String: SharePoint Workspace settings)

[Disable Windows Sticky Notes]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\StickyNotes\Disabled (DWORD: 1 = Disable)

[Change Windows Sticky Notes Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\StickyNotes (String: Sticky Notes settings)

[Disable Windows Trusted Platform Module]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\TrustedPlatformModule\Disabled (DWORD: 1 = Disable)

[Change Windows Trusted Platform Module Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\TrustedPlatformModule (String: Trusted Platform Module settings)

[Disable Windows UWP Apps]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\UWPApps\Disabled (DWORD: 1 = Disable)

[Change Windows UWP Apps Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\UWPApps (String: UWP Apps settings)

[Disable Windows Windows Search]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsSearch\Disabled (DWORD: 1 = Disable)

[Change Windows Windows Search Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsSearch (String: Windows Search settings)

[Disable Windows Windows Subsystem for Linux]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WSL\Disabled (DWORD: 1 = Disable)

[Change Windows Windows Subsystem for Linux Settings]
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\WSL (String: Windows Subsystem for Linux settings)
"""