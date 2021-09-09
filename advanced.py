import os, wget
from termcolours import bcolors

def pacman_all_mirrors() -> list:
    u = 'y'
    if os.path.exists('pacmanmirrorlist'):
        print('pacmanmirrorlist exists, do you want to redownload?')
        u = input('(y/n) ')
    if u.lower() == "y":
        try:
            os.remove('pacmanmirrorlist')
        except OSError:
            print('No pacmanmirrorlist in $HOME detected, retrieving file')
        print('Connecting to https://archlinux.org')
        wget.download(
            'https://archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on')
        if os.path.exists('download.wget'):
            os.rename('download.wget', 'pacmanmirrorlist')
        else:
            raise ValueError('Cannot find downloaded data')
        print()
        print('Downloaded, proccessing data')
        print('Done, saved in ' + os.getcwd())
    elif u.lower() == "n":
        print('Reading locally saved file in ' + bcolors.HEADER + os.getcwd() + bcolors.ENDC)
    with open('pacmanmirrorlist') as p:
        mirror = p.read().split('\n')
        mirrors = list(n.replace("#Server = ", "")[:n.index("/$") - 9] for n in list(
            m for m in mirror if '##' not in m and '!' not in m) if len(n) >= 3)
    print(bcolors.HEADER + 'Finished proccessing mirrors, now all of them will be sorted accordingly\nThis should take a while but no longer than ' +
           f'{len(mirrors)*13} seconds\nYou can also disable unwanted mirrors by adding ' + bcolors.ENDC +
           bcolors.WARNING+ '!' + bcolors.ENDC + bcolors.HEADER +' at the begining of the line' + bcolors.ENDC)
    return mirrors