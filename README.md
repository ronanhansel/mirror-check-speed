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
* Add "!" or "#" in front of the mirrors you don't want to check, the script will ignore those lines
# Supported package managers
* ~~Only pacman is known to be working in perfect state with current presets at the moment, to add more, you can contribute by modify the request url in main to enable more package managers~~ Supports all package managers although more testing needed.

# Well-tested mirrors
Here are the list of mirrors I tested myself, pretty much most of pacman mirrors' are supported because of the similariy of the request url
* chaotic-aur
* All mirrors in `/etc/pacman.d/mirrorlist`
* Almost all pacman mirrors (I might be wrong but you can try it)
* Almost mirrors from any package managers (Again more testing needed)

# Contribute
The module is very simple and easy to use and maintain, feel free to make a pull request. I'll try to elaborate as much as possible in my code with comments.
# Some images
![Screenshot_20210912_153930](https://user-images.githubusercontent.com/64572619/132980151-2bf71ceb-33c5-430c-9675-4da00496d208.png)
![Screenshot_20210912_153946](https://user-images.githubusercontent.com/64572619/132980156-4a2ba130-c3ce-4614-8eb8-51b1cb1bc6ca.png)
![Screenshot_20210912_154012](https://user-images.githubusercontent.com/64572619/132980158-a19ae465-eea1-411c-8abf-5ec6bc433ff9.png)

