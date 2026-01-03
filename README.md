# ⏳ County: Terminal Countdown Timer

> **A simple, zero-dependency countdown timer for your terminal.**

![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

I needed a big, readable timer for the terminal without dealing with GUI bloat or installing weird dependencies. **County** is just a simple Python script that displays a countdown in large ASCII digits.

It works out of the box on Windows, Mac, and Linux. It also flashes colors when you add or remove time so you have visual confirmation that your input registered.

---

## 📸 Demo

<p align="center">
  <img src="./assets/demo.gif" alt="Demo">
</p>

---

## 🎯 What it does

* **Big Display:** Shows the time in large ASCII characters.
* **Visual Feedback:** Flashes **Green** when you add time and **Red** when you remove it.
* **Panic Mode:** The whole timer flashes Red/White when there are less than 10 minutes left.
* **Intervals:** Gives a quick red flash every 30 minutes to help you keep track of long durations.
* **Safety:** It won't let you add time past the original duration (no overruns).

---

## ✨ Why use this?

* **No PIP Install:** It uses standard Python libraries only. Just download the script and run it.
* **No Flicker:** I spent some time fixing the rendering so the cursor hides properly and the text doesn't strobe.
* **Flexible Input:** It understands inputs like `60`, `60:00`, or `01:00:00`.
* **Cross-Platform:** I added specific handling for Windows CMD so the colors work properly there too.

---

## 🚀 Installation

Since there are no external dependencies, you just need the file.

    # Clone the repository
    git clone https://github.com/oNxZero/county.git

    # Enter the directory
    cd county

    # Make executable (optional, Linux/macOS)
    chmod +x county.py

---

## 📖 Usage

### Interactive Mode
Just run the script. It'll show an intro screen and ask you how long the timer should be.

    python county.py

### Fast-Start (CLI Flags)
Skip the intro and start the timer immediately.

    # Start a 60-minute timer
    python county.py -d 60:00

    # Start a 1-hour, 30-minute timer
    python county.py --duration 01:30:00

### Command Line Help
You can see all options right in the terminal:

    $ python county.py -h

    Usage:
      county [-d DURATION]
      county -h | --help

    Flags:
      -d,  --duration TIME    Start immediately with specific duration (HH:MM:SS or MM:SS)
      -h,  --help             Show this help and exit

    Controls:
      [UP] / [DOWN]           Add or subtract 5 minutes
      [SPACE]                 Pause or Resume
      [R]                     Reset timer
      [ESC]                   Quit

---

## 🎮 Controls

Make sure the terminal window is focused, then use these keys:

| Key | Action | Description |
| :--- | :--- | :--- |
| **[UP]** | **+5 Minutes** | Adds time. Screen flashes green. |
| **[DOWN]** | **-5 Minutes** | Removes time. Screen flashes red. |
| **[SPACE]** | **Pause / Resume** | Pauses the timer and shows a banner. |
| **[R]** | **Reset** | Resets the timer back to the start. |
| **[ESC]** | **Quit** | Closes the script. |

---

## ⚙️ Configuration

Want to tweak the settings? Just open `county.py` and edit the constants at the top:

    FLASH_LAST_SECONDS = 5 * 60      # Start flashing panic mode at 5 minutes
    RED_INTERVAL = 30 * 60           # Flash red every 30 minutes
    ADJUST_STEP = 5 * 60             # Time to add/remove on keypress (seconds)
    SPEED = 1.0                      # 1.0 = real time (increase to test/debug)
    FLASH_FEEDBACK_DURATION = 0.5    # How long the screen flashes color on input

### Customizing ASCII Art
If you want to change the font, I generated the current one using **ANSI Shadow**. You can grab new ASCII strings here and paste them into the `DIGITS` variable in the script:

* **Generator:** [patorjk.com/software/taag](https://patorjk.com/software/taag/#p=display&f=ANSI+Shadow&t=s&x=none&v=4&h=4&w=80&we=false)
* **Font Used:** ANSI Shadow

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
