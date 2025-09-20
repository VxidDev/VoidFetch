# VoidFetch

VoidFetch is a Python-based system information tool. It fetches your system information and displays it in a colorful, terminal-friendly way, including ASCII art logos for your OS(ONLY FOR ARCH!).

---

## Features

- Display OS name, release, and architecture
- Show CPU, RAM, and disk usage with color-coded indicators
- Display GPU information (VRAM usage)
- Show terminal, desktop environment, uptime, and boot time
- Showcase terminal colors
- ASCII logos for supported systems, with fallback logo
- Configurable via `config.json`(Limited)
- Optional debug mode for detailed info
- Generate example config easily

---

## Installation

Make sure you have Python 3.10+ installed. Then install required dependencies:

```bash
pip install psutil colorama GPUtil
```
Clone the repository:
```
git clone https://github.com/VxidDev/VoidFetch.git
cd VoidFetch
```
Install using pip:
```
pip install .
```
### Run normally
```
voidfetch
```

### Generate default config file
```
voidfetch --generate-config
```

### Enable debug mode
```
voidfetch --debug
```

## Config

By default, VoidFetch uses config.json to determine which system parameters to show:

```json
{
    "parameters": [
        "os-name",
        "os-release",
        "os-machine",
        "terminal",
        "shell",
        "desktop-enviroment",
        "boot_time",
        "uptime",
        "ram",
        "cpu",
        "disk",
        "gpu",
        "showcase-colors"
    ]
}
```
You can edit this file to customize which data is displayed.

Example output(might differ):
```
 ____   _______________     __         .__     
 \   \ /   /\_   _____/____/  |_  ____ |  |__  
  \   Y   /  |    __)/ __ \   __\/ ___\|  |  \ 
   \     /   |     \  ___/|  | \  \___|   Y  \
    \___/    \___  / \___  >__|  \___  >___|  /
             \/      \/          \/     \/ 

OS: Arch Linux
CPU: Intel Core i7-10750H: 12%
RAM: 8 GiB / 16 GiB
Disk: 250 GiB / 512 GiB
GPU 1: NVIDIA GTX 1650 - 2 GiB / 4 GiB
Terminal: xterm-256color
Desktop Enviroment: GNOME
Shell: bash 5.2
Uptime: 3 hours, 42 minutes
Boot Time: 2025-09-20 08:00:01
Colors: █🟧█🟨█🟩█🟦█🟪
```

### Created with ❤️ by VxidDev



