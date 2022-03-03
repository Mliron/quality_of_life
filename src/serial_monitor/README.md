# Serial monitor
Quick and dirty script that monitors traffic on a serial port (tested only on USB ports).

## Details
Requires [pyserial](https://github.com/pyserial/pyserial)
Connects to a serial port and prints out incoming traffic. Should be able to send text as well - anything you can type into the terminal.<br/>
You are able to specify which port to connect to - run `python3 serial_monitor.py --help` to get more information.

## Examples
`serial_monitor.py` - Connects to first open port or exits if there are no ports open<br/>
`serial_monitor.py -p /dev/ttyUSB1` - Tries to connect to port `/dev/ttyUSB1`. Exits if this port is not open.<br/>
`serial_monitor.py -l` - Waits and connects to the first open port.<br/>
`serial_monitor.py --listen -p /dev/ttyUSB1 ` - Waits and connects to port `/dev/ttyUSB1`.<br/>

## System compatibility
Linux-Ubuntu - Developed here - should work.
Windows - Should work, but not tried.
Raspberry Micropython - Should work, I used it there once.

## Plans for the future
- [ ] Add comments
