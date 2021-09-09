# mirror-check-speed
A simple python module for linux package managers which checks and reports fastest mirrors based on speed and latency
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
# Some actual pictures
![2021-09-09_10-59](https://user-images.githubusercontent.com/64572619/132620203-fbacedc8-3b04-435a-8c35-f679c67f2610.png)
![2021-09-09_11-00](https://user-images.githubusercontent.com/64572619/132620273-5c8f2201-2ede-4369-87ef-ba7fecae194e.png)
![2021-09-09_11-00_1](https://user-images.githubusercontent.com/64572619/132620334-155a33d1-02dc-4494-aebc-93a9d27cc6f5.png)
