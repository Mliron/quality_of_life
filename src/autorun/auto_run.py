#!/usr/bin/python3

import subprocess as sp
import os
import sys
from time import sleep as procrastinate
import argparse

c_compiler   = "gcc -std=c99"
cpp_compiler = "g++ -std=c++17"
c_cpp_flags  = "-O2 -g -pedantic -Wall -Wextra"
extensions = {
    "c"   : "c",
    "c++" : "cpp",
    "cpp" : "cpp",
    "py"  : "python",
    "pyw" : "python",
}


def check_timestamps(file_dict):
    updated = False
    for file in file_dict:
        tmp = os.path.getmtime(file)
        if file_dict[file] != tmp:
            file_dict[file] = tmp
            updated = True
    return updated

def get_shell_commands(arguments):
    compiled_name = None
    if arguments.command is not None and arguments.command != "":
        shell_input = (arguments.command)
    else:
        if arguments.language is None:
            arguments.language = extensions.get(arguments.FILE[0].split('.')[-1], arguments.FILE[0].split('.')[-1])
        if arguments.language == "c":
            shell_input = (f"{c_compiler} {c_cpp_flags} {' '.join(arguments.FILE)}")
            compiled_name = "./a.out"#f"./{'.'.join(args.file.split('.')[:-1])}"
        elif arguments.language == "c++" or arguments.language == "cpp":
            shell_input = (f"{cpp_compiler} {c_cpp_flags} {' '.join(arguments.FILE)}")
            compiled_name = "./a.out"#f"./{'.'.join(args.file.split('.')[:-1])}"
        elif arguments.language == "python":
            shell_input = (f"python {arguments.FILE[0]}")
        elif arguments.language == "python3":
            shell_input = (f"python3 {arguments.FILE[0]}")
        elif arguments.language == "python2":
            shell_input = (f"python2 {arguments.FILE[0]}")
        else:
            print(f"Unrecognised extension: {arguments.language}")
            print("You can specify language via '-l' option or specify a command to run via '-c' option.")
            return None
    if compiled_name is not None:
        return [shell_input, compiled_name]
    else:
        return [shell_input]

def main():
    parser = argparse.ArgumentParser(description="Keep track of one or multiple files and execute first given file or given command upon saving one of these files.")
    parser.add_argument("-l", "--language", choices=["c", "c++", "cpp", "python", "python3", "python2"], type=str,
                        help="(Optional) Specifies which language gets run. Parses extension by default.")
    parser.add_argument("-c", "--command",  type=str, help="Runs custom command when timestamp gets detected.")
    parser.add_argument("FILE", nargs="+",  type=str, help="File of which timestamp will be tracked.")
    args = parser.parse_args()

    files = {}
    for file in args.FILE:
        files[file] = os.path.getmtime(file)

    shell_input = get_shell_commands(args)
    if shell_input is None:
        return -1

    if args.command is not None:
        middle_piece = args.command.split(' ')[0]
    else:
        middle_piece = args.FILE[0].split('/')[-1]
    line = "".join(["=" for _ in range(22 - (len(middle_piece)>>1) - (len(middle_piece)&1))])
    additional = "=" if len(middle_piece)%2 else ""

    while True:
        if check_timestamps(files):
            print(f"\033[1m{line}{additional} \033[32m{middle_piece}\033[0m\033[1m {line}\033[0m")
            for command in shell_input:
                try:
                    sp.run(command.split(' '))
                except KeyboardInterrupt:
                    pass
            print("\033[1m==================== \033[31mDone\033[0m\033[1m ====================\033[0m")

        procrastinate(.2)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Hope you had fun! :)")
        sys.exit(0)
