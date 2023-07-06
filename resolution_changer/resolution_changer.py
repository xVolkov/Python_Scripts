# This script is for (SWDEV-385073) Display Settings Access ticket
# Script must run locally on target machine in order

import win32con #pip install pywin32
import win32api
import time
from screeninfo import get_monitors # pip install screeninfo

# Get all connected monitors' settings
def get_monitor_settings():
    monitors = get_monitors() # Get all connected monitors

    monitor_name_index = 1
    for monitor in monitors:
        resolution = f"{monitor.width}x{monitor.height}"
        print(f"\nMonitor {monitor_name_index}:")
        print(f"  Current resolution: {resolution}")
        print(f"  Primary monitor?: {monitor.is_primary}")

        if "5120x2880" in resolution:
            print("*** 5K monitor found! ***\n")
        monitor_name_index += 1

# Gets all available resolutions for each monitor connected to the system
# Returns: A Python nested list (2 levels) containing the monitor (level 1) and its available resolution settings (level 2)
def get_available_resolutions():
    resolutions = [] # A list containing the monitor name and its list of resolutions
    monitors = win32api.EnumDisplayMonitors() # Gets all monitors connected to the system

    for i, monitor in enumerate(monitors):
        monitor_name = f"Monitor {i + 1}"
        monitor_resolutions = [] # List to store the monitor's resolutions 

        device_name = win32api.GetMonitorInfo(monitor[0])['Device']
        devmode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)

        mode_index = 0
        while True:
            width = devmode.PelsWidth # Gets int pixel width of display
            height = devmode.PelsHeight # Gets int pixel height of display
            refresh_rate = devmode.DisplayFrequency # Gets refresh rate
            monitor_resolutions.append((width, height, refresh_rate)) # Append width, height, and refresh rate of the monitor to the list

            mode_index += 1 # Get next resolution setting for the monitor
            try:
                devmode = win32api.EnumDisplaySettings(device_name, mode_index)
            except:
                break
        monitor_resolutions = sorted(set(monitor_resolutions))

        resolutions.append((monitor_name, monitor_resolutions)) # append the monitor name and its list of resolutions

    return resolutions

# Change a specific monitor's resolution and refresh rate settings
def change_monitor_settings():
    available_resolutions = get_available_resolutions() # Function call to get available resolutions for each connected monitor (nested list)

    # Display available resolutions for each monitor
    print("\n------------------------------------------------")
    print("Available Resolutions:")
    print("------------------------------------------------")
    for monitor in available_resolutions:
        monitor_name = monitor[0]
        monitor_resolutions = monitor[1]
        
        print(f"  {monitor_name}:")
        for i, resolution in enumerate(monitor_resolutions): # Print monitor #s and their resolution indexes to choose from later
            print(f"    {i + 1}. Resolution: {resolution[0]}x{resolution[1]}, Refresh Rate: {resolution[2]}Hz")
        print()

    # Prompt the user to select a monitor and resolution
    while True:
        try:
            monitor_index = int(input("Enter the number of the monitor you want to change (e.g., 1, 2, 3): ")) 
            monitor_resolutions = available_resolutions[monitor_index - 1][1] # Stores user specified monitor index
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid monitor number.")

    while True:
        try:
            resolution_index = int(input("Enter the number of the resolution you want to set for your specified monitor: ")) 
            selected_resolution = monitor_resolutions[resolution_index - 1] # Stores user specified resolution in a tuple (width, height, refresh rate)
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid resolution number.")

    # Apply the user selected resolution to the specified monitor
    monitor_device = win32api.EnumDisplayMonitors()[monitor_index - 1][0] # Specifying the selected monitor by user
    devmode = win32api.EnumDisplaySettings(win32api.GetMonitorInfo(monitor_device)['Device'], win32con.ENUM_CURRENT_SETTINGS) # Accessing current settings of the specified monitor
    devmode.PelsWidth = selected_resolution[0]
    devmode.PelsHeight = selected_resolution[1]
    devmode.DisplayFrequency = selected_resolution[2]

    # Change the resolution
    result = win32api.ChangeDisplaySettingsEx(win32api.GetMonitorInfo(monitor_device)['Device'], devmode)
    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        

        # Check the new resolution
        new_resolution = win32api.EnumDisplaySettings(win32api.GetMonitorInfo(monitor_device)['Device'],
                                                        win32con.ENUM_CURRENT_SETTINGS)
        if (
                new_resolution.PelsWidth == selected_resolution[0]
                and new_resolution.PelsHeight == selected_resolution[1]
                and new_resolution.DisplayFrequency == selected_resolution[2]
        ):
            print(f"\n*** Resolution {i + 1}: {selected_resolution[0]}x{selected_resolution[1]}, Refresh Rate: {selected_resolution[2]}Hz - Successfully applied ***")
        else:
            print("\n*** Resolution change verification failed! ***")
        
    else:
        print(f"\n*** Resolution {i + 1}: {selected_resolution[0]}x{selected_resolution[1]}, Refresh Rate: {selected_resolution[2]}Hz - Failed to apply ***")
    
    time.sleep(2)

def main():
    while True:
        get_monitor_settings()
        user_input = input("\nEnter 'c' to change a monitor's resolution, else enter 'e' to exit the script: ") # Storing user input
        if user_input == "c":
            change_monitor_settings()
        elif user_input == "e":
            print("Exiting the script..")
            break
        else:
            print("ERROR, invalid input")
    return SystemExit

if __name__ == '__main__':
    print("\nChecking for connected monitors..")  
    main()