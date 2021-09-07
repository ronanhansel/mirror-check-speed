#!/usr/bin/python3

from ctypes import ArgumentError
import os
import sys
from time import time
from multiprocessing import Process, Value

results = {}
sort = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# This can stay intact, this function is simply for receiving test package ie alacritty
def get(n, start, lat, d, link):
    import requests
    file_name = "data.temp"
    print("Testing " + bcolors.OKBLUE +
          bcolors.BOLD + d + bcolors.ENDC)
    lat_start = time()
    response = requests.get(link, stream=True)
    lat_end = time()
    lat.value = lat_end - lat_start

    total_length = response.headers.get('content-length')
    with open(file_name, "wb") as f:
        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            start.value = time()
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                n.value = dl
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s] %.2f kB/%.2f kB" % ('=' *
                                 done, ' ' * (50-done), (dl/1024), (total_length/1024)))
                sys.stdout.flush()

# This is where you can modify to further support more package managers
def run(arg):
    # You can add more preset packages here
    pkgs = ['chaotic-aur/x86_64/alacritty-git-0.9.0.1850.g4a3bcdb4-1-x86_64.pkg.tar.zst',
            'community/os/x86_64/alacritty-0.9.0-1-x86_64.pkg.tar.zst']
    dire = '/etc/pacman.d/' # Default mirror directory for pacman, you shouldn't change this
    quest = input("Your mirrors' directory is: " + bcolors.HEADER + dire + bcolors.ENDC + " Correct? \n(y/n): ")
    # Selection menus
    while True:
        if quest.lower() == "y":
            break
        elif quest.lower() == "n":
            dire = input('input yours instead: ')
            if dire == '/etc/pacman.d/': print("That's just the same xD")
            break
        else:
            print("Please enter a valid option")
            quest = input(": ")
    files = os.listdir(dire)
    for i, k in enumerate(files):
        print(f"{i}. {k}")
    print("Type any letter to exit")
    opt = input("Select test mirror file: ")
    try:
        opt = int(opt)
    except Exception:
        return
    files = files[opt]
    for i, k in enumerate(pkgs):
        print(f"{i}. {k}")
    print(bcolors.WARNING + "If there's any error with your test, this might be why. Try changing package to see if it's the problem " +
          "\nOr you can search manually and paste the url here, " + 
          "\nplease note the valid url would look something like $repo/os/$package or $repo/$package" +
           bcolors.BOLD + "\nDO NOT" + bcolors.ENDC + bcolors.WARNING + " include host url" + bcolors.ENDC)
    try:
        usr = input("Select test packages url(integer) or enter your own(string): ")
        target = int(usr)
        pkg = pkgs[target]
    except Exception:
        pkg = usr
    with open(f'{dire}{files}', 'r') as file:
        data = file.read().replace('\n', ';').replace(";;", ";")

    data = data.split(";")
    data = list(a.replace("Server = ", "").replace(" ", "")[:a.index('$') - 9]
                for a in list(i for i in data if i != "") if a[0] != "#")

    for d in data:
        num = Value('d', 0.0)
        start = Value('d', 0.0)
        latency = Value('d', 0.0)
        p = Process(target=get, args=(num, start, latency, d, d + pkg))
        p.start()
        p.join(timeout=13)
        p.terminate()
        end = time()
        l = latency.value
        delta = end - start.value
        speed_pure = int(num.value/1024) / delta
        speed = "%.2f kB/sec" % (
            speed_pure) if speed_pure < 1024 else "%.2f MB/sec" % (speed_pure / 1024)
        # The connection is marked as Failed after 13 seconds if there's no response
        if speed_pure == 0.0:
            speed = bcolors.FAIL + bcolors.BOLD + "Failed" + bcolors.ENDC
            l = ""
        else:
            l = "{:.2f}".format(latency.value)
        print(f" -- {speed}")
        # Initialise the dictionary
        results[d] = {
            'latency': l,
            'speed': 0
        }
        results[d]['speed'] = speed
        if arg == '-s':
            sort[d] = speed_pure
        elif arg == '-l':
            sort[d] = latency.value
        
    return dict(sorted(sort.items(), key=lambda item: item[1])), results


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise ArgumentError('Missing argument')
    else:
        arg = sys.argv[1]
        if not arg in ["-l", "-s"]:
            raise ArgumentError("Incorrect argument passed")
    place = run(arg)
    print(bcolors.HEADER + bcolors.BOLD + "{:<3} {:<40} {:<20} {}".format(
        'N', 'Mirrors', 'Avg speed', 'Latency') + bcolors.ENDC)
    try:
        if arg == "-s":
            pl = reversed(place[0])
        elif arg == "-l":
            pl = place[0]
        for i, k in enumerate(pl):
            print("{:<3} {:<40} {:<20} {}" .format(
                i + 1, k, place[1][k]['speed'], place[1][k]['latency']))
        if os.path.exists('data.temp'):
            os.remove('data.temp')
    except TypeError:
        if os.path.exists('data.temp'):
            os.remove('data.temp')
        print('Exited')
