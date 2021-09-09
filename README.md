# mirror-check-speed
A simple python module for linux package managers which check and report fastest mirrors based on speed and latency
# Usage 
`python main.py <argument>`
### Available arguments
### Mandatory arguments
* `-s` : Sort mirrors by speed
* `-l` : Sort mirrors by latency
### Optional arguments
* `a`: Advanced mode, retrieve all available mirrors from AUR (for pacman only)
* `g`: Generate mirrorlist, sorted based on the result, highly experimental, only proceed if you know what you're doing
### Tips
* Add "!" in front of the mirrors you don't want to check, the script will ignore those lines
# Supported package managers
* Only pacman is known to be working in perfect state with current presets at the moment (I use Arch btw), to add more, you can contribute by modify the request url in main to enable more package managers
* Almost all package managers can be supported if you enter the url for custom package path and if the mirror file splits host url with a dollar sign ("$")

# Well-tested mirrors
Here are the list of mirrors I tested myself, pretty much most of pacman mirrors' are supported because of the similariy of the request url
* chaotic-aur
* All mirrors in `/etc/pacman.d/mirrorlist`
* Almost all pacman mirrors (I might be wrong but you can try it)

# Contribute
The module is very simple and easy to use, understand and maintain, you can add more mirrors by modifying the request urls. I'll try to elaborate as much as possible in my code with comments.
