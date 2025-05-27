[![Twitter: @NorowaretaGemu](https://img.shields.io/badge/X-@NorowaretaGemu-blue.svg?style=flat)](https://x.com/NorowaretaGemu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
  <br>
<div align="center">
  <a href="https://ko-fi.com/cursedentertainment">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="ko-fi" style="width: 20%;"/>
  </a>
</div>
  <br>

<div align="center">
  <img alt="Python" src="https://img.shields.io/badge/python%20-%23323330.svg?&style=for-the-badge&logo=python&logoColor=white"/>
</div>
<div align="center">
    <img alt="Git" src="https://img.shields.io/badge/git%20-%23323330.svg?&style=for-the-badge&logo=git&logoColor=white"/>
  <img alt="PowerShell" src="https://img.shields.io/badge/PowerShell-%23323330.svg?&style=for-the-badge&logo=powershell&logoColor=white"/>
  <img alt="Shell" src="https://img.shields.io/badge/Shell-%23323330.svg?&style=for-the-badge&logo=gnu-bash&logoColor=white"/>
  <img alt="Batch" src="https://img.shields.io/badge/Batch-%23323330.svg?&style=for-the-badge&logo=windows&logoColor=white"/>
  </div>
  <br>

# KIDA: Kinetic Interactive Drive Automaton

Rasberry Pi 5 Robot

OS:
Rasberry OS [Recommended!] (you can use any distro you choose)

Parts:

- Robot Tank Chassis (XiaoR Geek [Recommended!])
- L298N Motor Driver
- Rasberry Pi 5/4
- Pi Speakers
- 3x 16850 Pi UPS*
- Pi NVME + AI Hat
- 1x Pi 5 Nightvision Camera
- 1x Pi 5 AI Camera Camera
- 2x Pi Camera Holder
- Servo Motor
- NVME
- HAILO 13 TOPS
- 1x Ultrasonic Senser
- 2 x Power Switches
- DuPont Cables
- 3x 21700 Batteries
- 3 21700 Batterholder
- 3x 16850 Batteries*
- 1 USB Microphone
- 22 AWG Wire (21700 Battery Pack to L298N)

Electonic Schematic:

```bash
[12V Battery Pack 3S 21700 Battery 3.7v]
 ├── + ─────────► L298N VS       (motor power input)
 ├── + ─────────► LM2596S IN+    (step-down input for Pi)
 ├── – ─────────► L298N GND
 └── – ─────────► LM2596S IN–

[LM2596S Output]
 ├── OUT+ ──────► Pi 5V (GPIO pin 2 [[Not Recommended!] Pi UPS via USB-C cable [Recommended!]])
 └── OUT– ──────► Pi GND (GPIO pin 6 or 9)
```

## How to Run:

### Install Requirements

Using Python directly:

```bash
pip install -r requirements.txt
```
Or run: 
- `install_requirements.bat`

  
  <br>

```bash
  ~/.config/autostart
  ```

```bash
  nano ~/.config/autostart/kida.desktop
  ```

```bash
[Desktop Entry]
Name=KIDA Controller
Exec=python3 /home/pi/path/to/main.py
Type=Application
X-GNOME-Autostart-enabled=true
```

CRONTAB:

```bash
crontab -e
```
```bash
@reboot python3 /home/pi/path/to/main.py
```
```bash
sudo raspi-config
```

### Run main.py

Using Python directly:

```bash
python main.py
```

Using provided scripts:

Windows:
- `.\run.bat`
or
- `.\run.ps1`

Unix-like systems (Linux/macOS):
- `.\run.sh`

  <br>

## Requirements:

```bash

```

<br>
<div align="center">
© Cursed Entertainment 202*
</div>
<br>
<div align="center">
<a href="https://cursed-entertainment.itch.io/" target="_blank">
    <img src="https://github.com/CursedPrograms/cursedentertainment/raw/main/images/logos/logo-wide-grey.png"
        alt="CursedEntertainment Logo" style="width:250px;">
</a>
</div>
