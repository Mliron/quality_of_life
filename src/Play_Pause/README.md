# Software Play/Pause button
My notebook doesn't have media buttons, so I simulated the play/pause button with this script

## Details
Requires [xdotool](https://github.com/jordansissel/xdotool)<br/>
Requires [keyboard](https://github.com/boppreh/keyboard) module<br/>
Hooks an event to a key that will simulate the keypress.<br/>

Tbh I don't really like this implementation, but it is the only one that worked for me. If anyone has a better solution, please create an issue and let me know.

## Examples
`sudo python3 main.py` - Requires `sudo` because of the `keyboard` module

## Plans for the future
Probably not near future, I haven't touched this in a long time
- [ ] Make more user friendly
- [ ] Simulate more media buttons
- [ ] Hook onto wired headset media buttons
