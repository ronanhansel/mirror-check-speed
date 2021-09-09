# mirror-check-speed
A simple python module for linux package managers which checks and reports fastest mirrors based on speed and latency
# A brief intro
So you find out that your internet speed is extremely fast but when updating or installing any packages via terminal, it seems to be very slow, how come? 
Actually there's one common problem many would face is that the mirror configuration was incorrectly set up. 

There's a system file which lists all available online repository, the package manager would look it up everytime it installs any packages, the file is located in `/etc/pacman.d/mirrorlist` for pacman and `/etc/apt/sources.list` for apt) but the problem is that among dozens of different repos, sometimes the pac-man picks the unoptimised mirror for your location, you can fix that manually by edit the mirror file above with the help of this simple script.
# How this works ?
The script will read the mirror file which you specify or it detects and ignore all lines with comments "#" or exclamation mark "!", after that, it will try to download a package from the mirrors and measure it's speed.

The script can also modify mirror file (see `Usage` below) accordingly to the test result. Or just export them to your current working directory (cwd)

# Usage 
```
python main.py <arguments>
```
### Available arguments
#### Mandatory arguments
* `-s` : Sort mirrors by speed
* `-l` : Sort mirrors by latency
#### Optional arguments
* `a`: Advanced mode, retrieve all available mirrors from AUR (for pacman only)
* `g`: Generate mirrorlist, sorted based on the result and save in cwd or replace `/etc/pacman.d/mirrorlist` (highly experimental, only proceed if you know what you're doing)
#### Tips
* Add "!" in front of the mirrors you don't want to check, the script will ignore those lines
# Supported package managers
* ~~Only pacman is known to be working in perfect state with current presets at the moment, to add more, you can contribute by modify the request url in main to enable more package managers~~ Supports all package managers, more testing needed because I'm currently using Arch
* Almost all package managers can be supported if you enter the url for custom package path and if the mirror file splits host url with a dollar sign ("$")

# Well-tested mirrors
Here are the list of mirrors I tested myself, pretty much most of pacman mirrors' are supported because of the similariy of the request url
* chaotic-aur
* All mirrors in `/etc/pacman.d/mirrorlist`
* Almost all pacman mirrors (I might be wrong but you can try it)
* Almost mirrors from any package managers (Again more testing needed)

# Contribute
The module is very simple and easy to use and maintain, you can add more mirrors by modifying the request urls. I'll try to elaborate as much as possible in my code with comments.
# Some actual pictures
![2021-09-09_17-56](https://user-images.githubusercontent.com/64572619/132673995-6237ecb9-9c7e-4975-91a2-646161b6859f.png)
![2021-09-09_17-58](https://user-images.githubusercontent.com/64572619/132674093-8b1c9a30-d74c-406e-8ddd-56d531aa7e67.png)
![2021-09-09_17-59](https://user-images.githubusercontent.com/64572619/132674156-621880d8-4d23-4db9-b3b3-9e2867828f22.png)
