import winreg

# Define the Registry path you want to list
registry_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render'

# Open the Registry key
try:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
except FileNotFoundError:
    print(f"Registry path not found: {registry_path}")
    exit(1)

# Enumerate the subkeys (directories) within the opened key
subkeys = []
index = 0
while True:
    try:
        subkey_name = winreg.EnumKey(key, index)
        subkeys.append(subkey_name)
        index += 1
    except OSError:
        break

# Close the Registry key
winreg.CloseKey(key)


# Create a class to represent devices
class Device:
    def __init__(self, subkey, name, description, default_value, devicename, isdefaultvalue):
        self.subkey = subkey
        self.name = name
        self.description = description
        self.default = default_value
        self.devicename = devicename
        self.isdefault = False  # Initialize isdefault to False
        self.isdefaultvalue = isdefaultvalue

    def __str__(self):
        return (f"Device ID: {self.subkey}\nDevice name: {self.devicename}\nName: {self.name}\n"
                f"Description: {self.description}\nDefault: {self.default}\nIs Default: {self.isdefault}")


# Create a list to store Device objects
devices = []

isdefaultvalue = None

# Find the maximum default value before creating Device objects
for subkey_name in subkeys:
    subkey_path = rf'{registry_path}\{subkey_name}'

    try:
        subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
    except FileNotFoundError:
        continue

    try:
        level0_value, _ = winreg.QueryValueEx(subkey, 'Level:0')
        level1_value, _ = winreg.QueryValueEx(subkey, 'Level:1')
        if level0_value == level1_value:
            default = level0_value
            if isdefaultvalue is None or default > isdefaultvalue:
                isdefaultvalue = default
        else:
            default = None

        subkey_path = rf'{registry_path}\{subkey_name}\properties'
        try:
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
        except FileNotFoundError:
            continue
        try:
            name, _ = winreg.QueryValueEx(subkey, '{b3f8fa53-0004-438e-9003-51a46e139bfc},6')
            description, _ = winreg.QueryValueEx(subkey, '{a45c254e-df1c-4efd-8020-67d146a850e0},2')
            devicename = f'{name} - {description}'
        except FileNotFoundError:
            continue
        finally:
            winreg.CloseKey(subkey)

        # Create an instance of the Device class and append it to the devices list
        device = Device(subkey_name, name, description, default, devicename, isdefaultvalue)
        devices.append(device)
    except FileNotFoundError:
        continue

# Find the device with the highest default value and set its isdefault attribute to True
if devices:
    highest_default_device = max(devices, key=lambda x: x.default)
    highest_default_device.isdefault = True

# Print all devices
for device in devices:
    print(device)
