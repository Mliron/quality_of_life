import json
from datetime import datetime as dt
from datetime import timedelta
import sys
import argparse

this_dir = "/home/matus/Desktop/Programs/Personal/quality_of_life_repository/src/clockout/"
data_file = this_dir+"data/clockout_data.json"


def strfdelta(timestamp:timedelta):
    def pad(num:int):
        return str(num) if num>9 else '0'+str(num)
    days             = timestamp.days
    hours,   mod     = divmod(timestamp.seconds, 3600)
    minutes, seconds = divmod(mod, 60)
    return f"{pad((days*24)+hours)}:{pad(minutes)}:{pad(seconds)}"

def find(tag:str, pattern:str, do_sum:bool):
    try:
        with open(data_file, "r") as f:
            times = json.load(f)
    except FileNotFoundError:
        print("File not found!")
        return
    except json.JSONDecodeError:
        print("File is empty or corrupted!")
        return

    pattern  = pattern.replace(".", "-")
    def find_tagged(tagged:list, prefix:str):
        time_sum   = 0
        for item in tagged:
            index = item["start"][:11].find(pattern)
            if index == -1: continue
            if item["finish"] == None: timestamp = dt.now() - dt.strptime(item["start"], "%d-%m-%Y %H:%M:%S")
            else:                      timestamp = dt.strptime(item["finish"], "%d-%m-%Y %H:%M:%S") - dt.strptime(item["start"], "%d-%m-%Y %H:%M:%S")
            if do_sum: time_sum += timestamp.total_seconds()
            print(f"{prefix}==========================================")
            print(f"{prefix}{item['start'][:index]}\033[31m{item['start'][index:index+len(pattern)]}\033[0m{item['start'][index+len(pattern):]} -> {'Now' if item['finish'] == None else item['finish']}")
            print(f"{prefix}Session time: \033[33m{strfdelta(timestamp)}\033[0m")
        print(f"{prefix}==========================================")
        if do_sum:
            print(f"{prefix}Total elapsed time: \033[33m{strfdelta(timedelta(seconds=time_sum))}\033[0m")

    if tag == "None":
        for one_tag in times:
            print(f"Tag: '{one_tag}'")
            find_tagged(times[one_tag], "  ")
    else:
        find_tagged(times.get(tag, []), "")

def list_times(tag:str, num:int, do_sum:bool):
    try:
        with open(data_file, "r") as f:
            times = json.load(f)
    except FileNotFoundError:
        print("File not found!")
        return
    except json.JSONDecodeError:
        print("File is empty or corrupted!")
        return

    def list_tagged(tagged:list, prefix:str):
        time_sum   = 0
        item_count = 0
        if num > 0: item_count = -min(num, len(tagged))
        else:       item_count = 0
        for item in tagged[item_count:]:
            if item["finish"] == None: timestamp = dt.now() - dt.strptime(item["start"], "%d-%m-%Y %H:%M:%S")
            else:                      timestamp = dt.strptime(item["finish"], "%d-%m-%Y %H:%M:%S") - dt.strptime(item["start"], "%d-%m-%Y %H:%M:%S")
            if do_sum: time_sum += timestamp.total_seconds()
            print(f"{prefix}==========================================")
            print(f"{prefix}{item['start']} -> {'Now' if item['finish'] == None else item['finish']}")
            print(f"{prefix}Session time: \033[33m{strfdelta(timestamp)}\033[0m")
        print(f"{prefix}==========================================")
        if do_sum:
            print(f"{prefix}Total elapsed time: \033[33m{strfdelta(timedelta(seconds=time_sum))}\033[0m")
        print()

    if tag == "None":
        for one_tag in times:
            print(f"Tag: '{one_tag}'")
            list_tagged(times[one_tag], "  ")
    else:
        list_tagged(times.get(tag, []), "")

def toggle(tag:str):
    # Open file
    try:
        f = open(data_file, "r+")
    except FileNotFoundError:
        f = open(data_file, "w+")

    # Load JSON
    try:
        times = json.load(f)
    except json.decoder.JSONDecodeError:
        times = {}

    # Write new entry
    tagged = times.get(tag, None)
    if tagged is None:
        times[tag] = [{"start": dt.now().strftime("%d-%m-%Y %H:%M:%S"), "finish": None}]
        print(f"Clockout toggle: Started")
    else:
        if times[tag][-1]["finish"] is None:
            times[tag][-1]["finish"] = dt.now().strftime("%d-%m-%Y %H:%M:%S")
            print(f"Clockout toggle: Finished")
        else:
            times[tag].append({"start": dt.now().strftime("%d-%m-%Y %H:%M:%S"), "finish": None})
            print(f"Clockout toggle: Started")

    # Write to file
    f.seek(0)
    json.dump(times, f, indent=4)
    f.close()

def main():
    parser = argparse.ArgumentParser(description="Tool to time stuff")
    parser.add_argument("-t", "--tag", default="None",      help="Tag of timed action (for filtration)")
    parser.add_argument("--toggle", action="store_true",    help="Start or finish timing for given tag")
    parser.add_argument("--list-tags", action="store_true", help="Lists all existing tags")
    parser.add_argument("-l", "--list", nargs="?", metavar="N", type=int, const=-1,
                                                            help="List last N intervals for given tag (all if N is not specified)")
    parser.add_argument("-f", "--find", metavar="PATTERN",  help="Find PATTERN in start time for given tag")
    parser.add_argument("-s", "--sum", action="store_true", help="Sum of all found intervals. Used only with -f or -l")
    args = parser.parse_args()

    if (len(sys.argv) < 2)                                                                              \
       or (args.toggle and ((args.list is not None) or (args.find is not None)) and not args.list_tags) \
       or ((args.find is not None) and (args.list is not None) and not args.list_tags):
        parser.print_help()
        return

    if args.toggle:
        toggle(args.tag)
    elif args.list is not None:
        list_times(args.tag, args.list, args.sum)
    elif args.find is not None:
        find(args.tag, args.find, args.sum)
    elif args.list_tags:
        try:
            with open(data_file, "r") as f:
                times = json.load(f)
                print(list(times.keys()))
        except FileNotFoundError:
            print("File not found!")
            return
        except json.JSONDecodeError:
            print("File is empty or corrupted!")
            return
    else:
        args.print_help()


if __name__ == '__main__':
    main()
