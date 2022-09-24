#!/usr/bin/python3

import os
import sys
import requests
from advanced import pacman_all_mirrors
from time import time
from multiprocessing import Process, Value
from ctypes import ArgumentError
from termcolours import bcolors

# For better user experience when using the script, when debugging this line can be commented
# but this must not be commented upon commits
sys.tracebacklimit = 0

# initialise dicts

results = {}
sort = {}

# Various abbreviations
prompt = bcolors.OKGREEN + "⇁ " + bcolors.ENDC
total = 0

def print_list(arr: list):
    for i, k in enumerate(arr):
        print(prompt + f"{i}. {k}")


# This can stay intact, this function is simply for receiving test package ie alacritty
def get(n, start, lat, d, link, i):
    file_name = "data.temp"
    print(f"{i + 1}/{total} {prompt}" + bcolors.OKBLUE +
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
                sys.stdout.write("\r[%s%s] %.2f kB/%.2f kB" % ('█' *
                                 done, ' ' * (50-done), (dl/1024), (total_length/1024)))
                sys.stdout.flush()

# This is where you can modify to further support more package managers


def run(arg):
    try:
        if not 'a' in arg:
            dire = '/etc/pacman.d/'  # Default mirror directory for pacman, you shouldn't change this
            quest = input("Default mirror directory is: " +
                          bcolors.HEADER + dire + bcolors.ENDC + " Do you want to change?\n(y/n): ")
            # Selection menus
            while True:
                if quest.lower() == "n":
                    break
                elif quest.lower() == "y":
                    dire = input('input yours instead: ')
                    if dire == '/etc/pacman.d/':
                        print("That's just the same xD")
                    break
                else:
                    print("Please enter a valid option")
                    quest = input(": ")
            files = os.listdir(dire)
            print_list(files)
            print("Type any letter to exit")
            opt = input("Select test mirror file: ")
            try:
                opt = int(opt)
            except Exception:
                return
            files = files[opt]
            with open(f'{dire}{files}', 'r') as file:
                data = file.read().replace('\n', ';').replace(";;", ";")

            data = data.split(";")
            or_link = list(a.replace("Server = ", "").replace(" ", "")
                        for a in list(i for i in data if i != "") if a[0] != "#")
            data = list(a[:a.index('$')] for a in or_link)
            origin = dict(zip(data, or_link))
        else:
            print(
                'Advanced mode enabled, testing all available mirrors in https://archlinux.org')
            data = pacman_all_mirrors()
            print('Do you want to continue?')
            ip = input('(any/n): ')
            if ip == "n":
                return
        # You can add more preset packages here
        pkgs = ['community/os/x86_64/alacritty-0.9.0-1-x86_64.pkg.tar.zst',
                'chaotic-aur/x86_64/alacritty-git-0.9.0.1850.g4a3bcdb4-1-x86_64.pkg.tar.zst']
        print_list(pkgs)
        print(bcolors.WARNING + "Try changing package if there's problem " +
              "\nOr you can search manually and paste the url here, " +
              bcolors.BOLD + "\nDO NOT" + bcolors.ENDC + bcolors.WARNING + " include host url" + bcolors.ENDC)
        try:
            usr = input(
                "Select test packages url(integer) or enter your own(string): ")
            target = int(usr)
            pkg = pkgs[target]
        except Exception:
            pkg = usr
        global total
        total = len(data)
        for i, d in enumerate(data):
            num = Value('d', 0.0)
            start = Value('d', 0.0)
            latency = Value('d', 0.0)
            p = Process(target=get, args=(num, start, latency, d, d + pkg, i))
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
            if 's' in arg:
                sort[d] = speed_pure
            elif 'l' in arg:
                sort[d] = latency.value
        reordered = dict(sorted(sort.items(), key=lambda item: item[1]))
        if "g" in arg:
            from generatemirror import makemrr
            makemrr(reversed(list(a for a in reordered)), origin)
        return reordered, results
    except KeyboardInterrupt:
        print('Interrupted')
        return dict(sorted(sort.items(), key=lambda item: item[1])), results


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise ArgumentError('Missing argument')
    else:
        arg = sys.argv[1]
        if arg[1] not in ["l", "s"]:
            raise ArgumentError("Incorrect argument passed")
    place = run(arg)
    print(bcolors.HEADER + bcolors.BOLD + "{:<3} {:<50} {:<20} {}".format(
        'N', 'Mirrors', 'Avg speed', 'Latency') + bcolors.ENDC)
    try:
        if "s" in arg:
            pl = reversed(place[0])
        elif "l" in arg:
            pl = place[0]
        for i, k in enumerate(pl):
            print("{:<3} {:<50} {:<20} {}" .format(
                i + 1, k, place[1][k]['speed'], place[1][k]['latency']))
        if os.path.exists('data.temp'):
            os.remove('data.temp')
    except TypeError:
        if os.path.exists('data.temp'):
            os.remove('data.temp')
        print('Exited')
