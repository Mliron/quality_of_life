#!/usr/bin/env python3
import serial
import serial.tools.list_ports as list_ports
from time import sleep as procrastinate
import sys
from select import select
import argparse

def printf(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()
print = printf

class SerialMonitor:
    def __init__(self, port, baudrate=115200, stdin_callback=None, callback=None, kwargs={}, reconnect=False, connect_if_closed=False):
        self.usb_port        = port
        self.baudrate        = baudrate
        self.serial          = None
        self.stdin_callback  = stdin_callback if stdin_callback is not None else self.exit
        self.callback        = callback if callback is not None else self.behavior
        self.callback_kwargs = kwargs
        self._connected      = False
        self.reconnect       = reconnect
        self.exit_keyword    = "exit\n"
        self.persist         = connect_if_closed

    def __del__(self):
        self.disconnect()

    def _get_stdin(self):
        data,_,_ = select([sys.stdin], [], [], 0.0001)
        if data != []:
            return data[0].readline()
        return None

    def connect(self, timeout=-1):
        timeout = int(timeout) + 0.5

        if self._connected:
            print("Port {} already connected.\n".format(self.usb_port))
            return

        print("Checking open ports")
        while True:
            open_ports = sorted(ports.device for ports in list_ports.comports())
            if not self.persist:
                print("\n")
                break
            if len(open_ports) > 0:
                if self.usb_port is not None:
                    if self.usb_port in open_ports:
                        print("\n")
                        break
                else:
                    print("\n")
                    break
            procrastinate(0.5)
            print(".")

        if self.usb_port is None:
            if len(open_ports) <= 0:
                print("No port is open\n".format(self.usb_port))
                return
            self.usb_port = open_ports[0]
        elif self.usb_port not in open_ports:
            print("Port '{}' not found.\n".format(self.usb_port))
            return

        print("Connecting to port: {}\n".format(self.usb_port))

        while timeout != 0:
            if self._get_stdin() == self.exit_keyword:
                return
            try:
                self.serial = serial.Serial(self.usb_port, self.baudrate)
            except serial.serialutil.SerialException:
                print(".")
                procrastinate(0.5)
                timeout -= 0.5
            else:
                print("\nConnected\n")
                self._connected = True
                break

        if not self._connected:
            print("Failed to connect to port {}\n".format(self.usb_port))

        return self._connected

    def disconnect(self):
        if self.serial is not None and self.serial.isOpen():
            self._connected = False
            self.serial.close()
            print("Port {} disconnected.\n".format(self.usb_port))

    def capture(self):
        stdin_input = None
        while self._connected:
            try:
                if self.serial.inWaiting():
                    self.callback(self.serial.readline(), **self.callback_kwargs)
            except OSError:
                print("Communications on port {} broke down.\n".format(self.usb_port))
                self.disconnect()
                if self.reconnect:
                    self.connect()

            stdin_input = self._get_stdin()
            if stdin_input is not None:
                stdin_input = self.stdin_callback(stdin_input)
                if self._connected:
                    self.serial.write(stdin_input.encode())

    def behavior(self, data, **kwargs):
        try:
            print(data.decode("ascii"))
        except UnicodeDecodeError:
            pass

    def exit(self, data):
        if data == self.exit_keyword:
            self.disconnect()
        else:
            return data
        return ""

def main():
    parser = argparse.ArgumentParser(description="Tool to view usb port traffic")
    parser.add_argument("-p", "--port", help="Specify which port to connect to.")
    parser.add_argument("-l", "--listen", action="store_true", help="Listen for a connection even if it's not connected.")
    args = parser.parse_args()

    monitor = SerialMonitor(args.port, reconnect=False, connect_if_closed=args.listen)
    try:
        import keyboard as kbd
        kbd.add_hotkey("ctrl+]", monitor.disconnect)
    except ImportError:
        print("Couldn't import keyboard module (not important)\n")
    monitor.connect()
    monitor.capture()

    print("Serial monitor ending\n")


if __name__ == "__main__":
    main()
