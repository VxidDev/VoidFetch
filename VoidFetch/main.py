import argparse # for parsing arguments 
import json # for config
import psutil # for getting system data!
from colorama import Style , Fore , init # for colored printing
import os # for linux cpu name
import subprocess # for command output
import datetime # for time
import sys # for exiting script fully
import platform # for system data
import GPUtil

init()

available_ascii = {
    "fallback": rf"""
    {Style.BRIGHT + Fore.BLACK}____   ____{Fore.WHITE}___________     __         .__     
    {Style.BRIGHT + Fore.BLACK}\   \ /   /{Fore.WHITE}\_   _____/____/  |_  ____ |  |__  
    {Style.BRIGHT + Fore.BLACK} \   Y   /{Fore.WHITE}  |    __)/ __ \   __\/ ___\|  |  \ 
    {Style.BRIGHT + Fore.BLACK}  \     /{Fore.WHITE}   |     \\  ___/|  | \  \___|   Y  \
    {Style.BRIGHT + Fore.BLACK}   \___/{Fore.WHITE}    \___  / \___  >__|  \___  >___|  /
    {Style.BRIGHT + Fore.BLACK}       {Fore.WHITE}         \/      \/          \/     \/ 
    {Style.RESET_ALL}""",

    "Arch Linux": r"""
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++.
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `""" + Style.RESET_ALL
}
default_config = {
    "parameters": ["os-name" , "os-release" , "os-machine" , "terminal" , "shell" , "desktop-enviroment" , "boot_time" , "uptime", "ram" , "cpu" , "disk", "gpu" , "showcase-colors"]
}

available_parameters = {
    "ram": psutil.virtual_memory, 
    "cpu": {
        "core_amount": psutil.cpu_count,
        "core_usage": lambda: psutil.cpu_percent(interval=5 , percpu=True)
    },
    "disk": lambda: psutil.disk_usage("/"),
    "boot_time": psutil.boot_time,
    "uptime": subprocess.run("uptime -p" , shell=True , capture_output=True , text=True).stdout,
    "os": {
        "name": lambda: platform.freedesktop_os_release()["PRETTY_NAME"],
        "system": lambda: platform.uname().system,
        "release": lambda: platform.uname().release, 
        "machine": lambda: platform.uname().machine
    },
    "gpu":{
        "all-gpus": GPUtil.getGPUs
    },
    "showcase-colors": Style.BRIGHT + Fore.RED + "█" + "\033[38;2;255;165;0m█\033[0m" + Fore.YELLOW + "█" + Fore.GREEN + "█" + Fore.BLUE + "█" + "\033[38;2;75;0;130m█\033[0m" + Fore.MAGENTA + Style.RESET_ALL,
    "terminal": lambda: subprocess.run("echo $TERM" , shell=True , capture_output=True , text=True).stdout.strip(),
    "desktop-enviroment": lambda: subprocess.run("echo $XDG_CURRENT_DESKTOP" , shell=True , capture_output=True , text=True).stdout.strip(),
    "shell": lambda: os.path.basename(os.environ["SHELL"])
}

def print_message(message , message_type: str = None):
    if message_type is not None:
        if message_type == "warn":
            color = Fore.YELLOW
        elif message_type == "error":
            color = Fore.RED
        elif message_type == "success":
            color = Fore.GREEN
        elif message_type == "info":
            color = Fore.WHITE
        else:
            color = Fore.RED
            message = f"'{message_type}' is not a valid message type!"
            message_type = "error"
    print(Style.BRIGHT + color + f"{message_type}: " + Style.RESET_ALL + message)

def get_ascii(debug=False):
    global ascii
    if debug:
        print_message("choosing ascii depending on OS name..." , "info")
    try:
        os_color = platform.freedesktop_os_release()["ANSI_COLOR"]
    except KeyError:
        if debug:
            print_message("'ANSI_COLOR' not found. Using white color." , "error")
        os_color = Fore.WHITE
    try:
        ascii = available_ascii[available_parameters["os"]["name"]()]
    except KeyError:
        if debug:
            print_message("ASCII logo not found. Using fallback logo..." , "error")
        ascii = available_ascii["fallback"]
    ascii = f"\033[{os_color}m{ascii}"
    if debug:
        print_message(f"Using {platform.freedesktop_os_release()["PRETTY_NAME"]}'s logo..." , "success")

def gen_config(debug=False):
    global config_data
    if debug:
        print_message("generating config..." , "info")
    with open("config.json" , "w") as config:
        json.dump(default_config , config)
    config_data = default_config
    if debug:
        print_message("config generated!" , "success")

def get_config_data(debug=False):
    global config_data
    if debug:
        print_message("Getting config data..." , "info")
    try:
        with open("config.json" , "r") as config:
            config_data = json.load(config)
        if debug:
            print_message("Config Data fetched successfully!" , "success")
            print(config_data)
    except FileNotFoundError:
        if debug:
            print_message("File not found! Re-generating config..." , "warn")
        gen_config(debug=debug)
    except json.JSONDecodeError:
        print_message("File corrupted! Do you want to regenerate config?" , "error")
        choice = ""
        while choice not in ("y" , "n"):
            choice = input("\nY/N: ").lower()
        if choice == "n":
            if debug:
                print_message("closing..." , "info")
            sys.exit()
        else:
            gen_config(debug=debug)

def get_ram_data(debug=False):
    if debug:
        print_message(str(available_parameters["ram"]()) , "success")
    total_ram = available_parameters["ram"]().total
    used_ram = total_ram - available_parameters["ram"]().available
    if debug:
          print_message("getting color based on ram usage..." , "info")
    if used_ram <= total_ram / 100 * 30:
        color = Fore.GREEN
    elif total_ram / 100 * 30 < used_ram <= total_ram / 100 * 75:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    if debug:
        print_message(f"{color}test{Style.RESET_ALL}" , "success")
    return Style.BRIGHT + "RAM: " + color + f"{round(used_ram / (1024 ** 3) , 2)} GiB / {round(total_ram / (1024 ** 3) , 2)} GiB\n" + Style.RESET_ALL

def get_cpu_data(debug=False):
    core_amount = available_parameters["cpu"]["core_amount"]()
    cpu_usage = round(sum(available_parameters["cpu"]["core_usage"]()) / (core_amount * 100) * 100 , 2)
    if os.name == "posix":
        if debug:
            print_message("linux user, getting cpu name..." , "info")
        cpu_name = subprocess.run("lscpu" , capture_output=True , text=True).stdout
        if debug:
            print_message("searching for cpu name in cpu_name.stdout..." , "success")
        for line in cpu_name.splitlines():
            if "Model name" in line:
                if debug:
                    print_message(line , "success")
                cpu_name = line.removeprefix("Model name:").strip()
    if debug:
        print_message(f"{core_amount , cpu_usage , cpu_name}" , "success")
        print_message("selecting color based on cpu usage..." , "info")
    if cpu_usage <= 30:
        color = Fore.GREEN
    elif 30 < cpu_usage <= 75:
        color = Fore.YELLOW
    else: 
        color = Fore.RED
    if debug:
        print_message(f"{color}test{Style.RESET_ALL}" , "success")
    return Style.BRIGHT + "CPU: " + color + f"{cpu_name}: {cpu_usage}%\n" + Style.RESET_ALL

def get_disk_data(debug=False):
    total_storage = round(available_parameters["disk"]().total / (1024 ** 3)) 
    storage_used = round(available_parameters["disk"]().used / (1024 ** 3) , 2) 
    if debug:
        print_message("selecting color based on storage usage..." , "info")
    if storage_used <= total_storage / 100 * 30:
        color = Fore.GREEN
    elif total_storage / 100 * 30 < storage_used <= total_storage / 100 * 75:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    if debug:
        print_message(f"{color}test{Style.RESET_ALL}" , "success")
    return Style.BRIGHT + "Disk: " + color + f"{storage_used} GiB / {total_storage} GiB\n" + Style.RESET_ALL

def get_boot_time(debug=False):
    boot_time = datetime.datetime.fromtimestamp(available_parameters["boot_time"]())
    if debug:
        print_message("boot time fetched!" , "success")
        print_message(str(boot_time) , "success")
    return Style.BRIGHT + Fore.WHITE + f"Boot Time: {boot_time}\n"

def get_os_data(param , debug=False):
    os_color = platform.freedesktop_os_release()['ANSI_COLOR']
    if debug:
        print_message(available_parameters["os"][param]() , "success")
    return f"{Style.BRIGHT + Fore.WHITE + param.capitalize()}: \033[{os_color}m{available_parameters['os'][param]()}\n"

def get_gpu_data(debug=False):
    gpus = available_parameters["gpu"]["all-gpus"]()
    for gpu in gpus:
        memory_total = round(gpu.memoryTotal / 1024 , 2)
        memory_used = round(gpu.memoryUsed / 1024 , 2)
        if debug:
            print_message(f"GPU {gpu.id + 1}: {gpu.name} - {memory_used} GiB / {memory_total} GiB" , "success")
            print_message("choosing color based on vram usage..." , "info")
        if memory_used <= memory_total / 100 * 30:
            color = Fore.GREEN 
        elif memory_total / 100 * 30 < memory_used <= memory_total / 100 * 75:
            color = Fore.YELLOW 
        else:
            color = Fore.RED 
    if debug:
        print_message("Done fetching gpu data!" , "success")
    return f"{Style.BRIGHT + Fore.WHITE}GPU {gpu.id + 1}:" + color + f" {gpu.name} - {memory_used} GiB / {memory_total} GiB{Style.RESET_ALL}\n"

def get_uptime_data(debug=False):
    uptime = available_parameters["uptime"].removeprefix("up").strip()
    if debug:
        print_message(uptime , "success")

    return Style.BRIGHT + Fore.WHITE + "Uptime: " + uptime + Style.RESET_ALL + "\n"

def get_terminal_data(debug=False):
    output = f"{Style.BRIGHT + Fore.WHITE}Terminal: {available_parameters["terminal"]() + Style.RESET_ALL}\n"
    if debug:
        print_message("Terminal data fetched!" , "success")
    return output

def get_desktop_enviroment_data(debug=False):
    output = f"{Style.BRIGHT + Fore.WHITE}Desktop Enviroment: {available_parameters["desktop-enviroment"]()}{Style.RESET_ALL}\n"
    if debug:
        print_message("Desktop Enviroment data fetched!" , "success")

    return output

def get_shell_data(debug=False):
    output = available_parameters["shell"]()
    if output == "bash":
        if debug:
            print_message("Getting bash version..." , "info")
        output += f" {subprocess.run("""bash --version | head -n1 | awk '{print $4}' | cut -d'(' -f1
""" , shell=True , capture_output=True , text=True).stdout.strip()}"
    if debug:
        print("Shell data fetched!" , "success")
    
    return Style.BRIGHT + Fore.WHITE + "Shell: " + output + "\n"

available_commands = {
    "ram": get_ram_data,
    "cpu": get_cpu_data,
    "disk": get_disk_data,
    "boot_time": get_boot_time,
    "uptime": get_uptime_data,
    "os": get_os_data,
    "gpu": get_gpu_data,
    "showcase-colors": available_parameters["showcase-colors"],
    "terminal": get_terminal_data,
    "desktop-enviroment": get_desktop_enviroment_data,
    "shell": get_shell_data
}

def get_system_info(parameter , debug=False):
    if debug:
        print_message(f"fetching {parameter} data..." , "info")
    if "os" in parameter:
        output = available_commands["os"](parameter.split("-")[1].strip() , debug=debug)
    elif "showcase-colors" in parameter:
        output = f"{Style.BRIGHT + Fore.WHITE}Colors: {Style.RESET_ALL}{available_commands[parameter]}\n"
    else:
        output = available_commands[parameter](debug=debug)
    
    return output

def main():
    global output
    parser = argparse.ArgumentParser(description="VoidFetch: A Neofetch alternative by VxidDev, made for learning argparser!")
    
    parser.add_argument("-gen-conf" , "--generate-config" , action="store_true" , help="Generate Example Config!")
    parser.add_argument("-d" , "--debug" , action="store_true" , help="Debug mode!")

    args = parser.parse_args()

    if args.generate_config:
        get_config_data(debug=args.debug)
    else:
        get_config_data(debug=args.debug) 

    get_ascii(debug=args.debug)

    print(ascii)
    output = ""
    for param in config_data["parameters"]:
        try:
            if "os" in param or param in available_parameters:
                output += get_system_info(param , debug=args.debug)
            else:
                print_message("Parameter not found, skipping..." , "warn")
        except Exception as e:
            print_message("Error while fetching data." , "error")
            print_message(str(e) , "error")
    print(output.strip())

if __name__ == "__main__":
    main()
