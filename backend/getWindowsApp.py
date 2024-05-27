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
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0].lower()

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0].lower()
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0].lower()
            except EnvironmentError:
                software['publisher'] = 'undefined'

            # Retrieve installation location if available
            try:
                install_location = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
                if install_location.strip():  # Check if the installation location is not empty
                    software['install_location'] = install_location.lower()
                    # Search for executable file within the installation directory
                    executable_file = find_executable(software['name'], install_location)
                    if executable_file:
                        software['executable_file'] = executable_file.lower()
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
                return os.path.join(root, file).lower()
    return None

software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)

file_path = 'apps.txt'

with open(file_path, 'w') as file:
    for software in software_list:
        if 'install_location' in software:
            line = f"{software['name']} || "
            if 'executable_file' in software:
                line += f"\"{software['executable_file']}\""
            else :
                line += f"\"nopath\""
            file.write(line + '\n')    

# Extract software names from apps.txt
software_names = []
with open(file_path, 'r') as file:
    for line in file:
        if ' || ' in line:
            software_name = line.split(' || ')[0]
            # Split the software name into words and add to the list
            software_names.extend(software_name.split())

# Update cfg_rules.txt with software names
cfg_rules_path = 'cfg_rules.txt'
with open(cfg_rules_path, 'r') as file:
    lines = file.readlines()

# Find the index of PROGRAM and ADJECTIVE lines
program_index = None
adjective_index = None
for i, line in enumerate(lines):
    if line.strip().startswith('PROGRAM ->'):
        program_index = i
    elif line.strip().startswith('ADJECTIVE ->'):
        adjective_index = i

# Update PROGRAM and ADJECTIVE lines with software names
if program_index is not None:
    lines[program_index] = 'PERSONAL_PROGRAM -> ' + ' | '.join(f'"{name}"' for name in software_names) + '\n'
if adjective_index is not None:
    lines[adjective_index] = 'PERSONAL_ADJECTIVE -> ' + ' | '.join(f'"{name}"' for name in software_names) + '\n'

# Write the updated lines back to cfg_rules.txt
with open(cfg_rules_path, 'w') as file:
    file.writelines(lines)

print("Successfully updated apps.txt and cfg_rules.txt")