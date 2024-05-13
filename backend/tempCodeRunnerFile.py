for software in software_list:
        file.write('%s || %s\n' % (software['name'], software.get('install_location', 'No install location')))
    file.write('Number of installed apps: %s' % len(software_list))