import subprocess
import sys
import time

try:
    import keyboard as kbd
except ImportError:
    print("You have to have root access.")
    sys.exit()

running = True

def send_cmd():
    subprocess.run("xdotool key --delay 0 XF86AudioPlay", shell=True)

def stop_script():
    global running
    running = False

def main():
    global running
    kbd.add_hotkey("`", send_cmd)
    # kbd.add_hotkey("ctrl+]", stop_script)
    while(running):
        time.sleep(15)


if __name__ == "__main__":
    main()
