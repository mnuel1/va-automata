import os
import winreg

def foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'

            # Retrieve installation location if available
            try:
                install_location = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
                if install_location.strip():  # Check if the installation location is not empty
                    software['install_location'] = install_location
                    # Search for executable file within the installation directory
                    executable_file = find_executable(software['name'], install_location)
                    if executable_file:
                        software['executable_file'] = executable_file
            except FileNotFoundError:
                pass

            if 'install_location' in software:
                software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def find_executable(app_name, install_location):
    for root, dirs, files in os.walk(install_location):
        for file in files:
            if file.lower().startswith(app_name.lower()) and file.lower().endswith('.exe'):
                return os.path.join(root, file)
    return None

software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

file_path = 'apps.txt'

with open(file_path, 'w') as file:
    for software in software_list:
        if 'install_location' in software:
            line = f"{software['name']} || {software.get('install_location', 'No install location')}"
            if 'executable_file' in software:
                line += f" || {software['executable_file']}"
            file.write(line + '\n')
    file.write('Number of installed apps: %s' % len(software_list))
