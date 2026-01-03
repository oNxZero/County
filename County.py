import time
import os
import shutil
import sys
import argparse

FLASH_LAST_SECONDS = 5 * 60         # Last X seconds to flash
RED_INTERVAL = 30 * 60               # Every X seconds show red
ADJUST_STEP = 5 * 60                 # +/- step in seconds
SPEED = 1.0                          # 1.0 = real time
FLASH_FEEDBACK_DURATION = 0.5        # Duration of Green/Red flash on input

CLEAR_CMD = "cls" if os.name == "nt" else "clear"

RED_ANSI = "\033[31m"      # paused, gameover, -minutes
GREEN_ANSI = "\033[32m"    # +minutes
WHITE_ANSI = "\033[37m"
RESET_ANSI = "\033[0m"

USE_ANSI_CLEAR = True

HELP_TEXT = """Usage:
  County [-d DURATION]
  County -h | --help

Flags:
  -d,  --duration TIME    Start immediately with specific duration (HH:MM:SS or MM:SS)
  -h,  --help             Show this help and exit

Controls:
  [UP] / [DOWN]           Add or subtract 5 minutes
  [SPACE]                 Pause or Resume
  [R]                     Reset timer
  [ESC]                   Quit

Examples:
  County
  County -d 10:00
  County --duration 01:30:00
"""

DIGITS = {
    "0": [
        " ██████╗ ",
        "██╔═████╗",
        "██║██╔██║",
        "████╔╝██║",
        "╚██████╔╝",
        " ╚═════╝ ",
        "         "
    ],
    "1": [
        " ██╗",
        "███║",
        "╚██║",
        " ██║",
        " ██║",
        " ╚═╝",
        "    "
    ],
    "2": [
        "██████╗  ",
        "╚════██╗ ",
        " █████╔╝ ",
        "██╔═══╝  ",
        "███████╗ ",
        "╚══════╝ ",
        "         "
    ],
    "3": [
        "██████╗  ",
        "╚════██╗ ",
        " █████╔╝ ",
        " ╚═══██╗ ",
        "██████╔╝ ",
        "╚═════╝  ",
        "         "
    ],
    "4": [
        "██╗  ██╗ ",
        "██║  ██║ ",
        "███████║ ",
        "╚════██║ ",
        "     ██║ ",
        "     ╚═╝ ",
        "         "
    ],
    "5": [
        "███████╗ ",
        "██╔════╝ ",
        "███████╗ ",
        "╚════██║ ",
        "███████║ ",
        "╚══════╝ ",
        "         "
    ],
    "6": [
        " ██████╗ ",
        "██╔════╝ ",
        "███████╗ ",
        "██╔═══██╗",
        "╚██████╔╝",
        " ╚═════╝ ",
        "         "
    ],
    "7": [
        "███████╗ ",
        "╚════██║ ",
        "    ██╔╝ ",
        "   ██╔╝  ",
        "   ██║   ",
        "   ╚═╝   ",
        "         "
    ],
    "8": [
        " █████╗  ",
        "██╔══██╗ ",
        "╚█████╔╝ ",
        "██╔══██╗ ",
        "╚█████╔╝ ",
        " ╚════╝  ",
        "         "
    ],
    "9": [
        " █████╗  ",
        "██╔══██╗ ",
        "╚██████║ ",
        " ╚═══██║ ",
        " █████╔╝ ",
        " ╚════╝  ",
        "         "
    ],
    ":": [
        "      ",
        "  ██  ",
        "      ",
        "      ",
        "  ██  ",
        "      ",
        "      "
    ],
}

INTRO_BANNER = [
    " ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗",
    "██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝",
    "██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝ ",
    "██║     ██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝  ",
    "╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║   ",
    " ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝   ",
]

PAUSED_BANNER = [
    "██████╗  █████╗ ██╗   ██╗███████╗███████╗██████╗ ",
    "██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗",
    "██████╔╝███████║██║   ██║███████╗█████╗  ██║  ██║",
    "██╔═══╝ ██╔══██║██║   ██║╚════██║██╔══╝  ██║  ██║",
    "██║     ██║  ██║╚██████╔╝███████║███████╗██████╔╝",
    "╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝ ",
    "                                                 ",
]

GAME_OVER = [
    "███████╗██╗  ██╗██████╗ ██╗██████╗ ███████╗██████╗ ",
    "██╔════╝╚██╗██╔╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗",
    "█████╗   ╚███╔╝ ██████╔╝██║██████╔╝█████╗  ██║  ██║",
    "██╔══╝   ██╔██╗ ██╔═══╝ ██║██╔══██╗██╔══╝  ██║  ██║",
    "███████╗██╔╝ ██╗██║     ██║██║  ██║███████╗██████╔╝",
    "╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝ ",
    "                                                   ",
]

def clear():
    if USE_ANSI_CLEAR and os.name != "nt":
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()
    else:
        os.system(CLEAR_CMD)

def get_term_size():
    return shutil.get_terminal_size((80, 24))

def center_block(block, term_w, term_h):
    if not block: return []
    bh = len(block)
    bw = max((len(l) for l in block), default=0)
    top = max(0, (term_h - bh) // 2)
    left = max(0, (term_w - bw) // 2)
    return ([""] * top) + [(" " * left + l) for l in block]

def print_block(block, color=RESET_ANSI):
    out = []
    prefix = color if color else ""
    for line in block:
        out.append(prefix + line + RESET_ANSI)
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

def render_time(text):
    height = len(next(iter(DIGITS.values())))
    lines = [""] * height
    for ch in text:
        art = DIGITS.get(ch, DIGITS[":"])
        for i in range(height):
            lines[i] += art[i] + "  "
    return lines

def parse_duration(time_str):
    if not time_str: return None
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = map(int, parts)
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = map(int, parts)
            return m * 60 + s
        elif len(parts) == 1:
            return int(parts[0])
    except ValueError:
        return None
    return None

_is_windows = (os.name == "nt")
_unix_old_settings = None
_unix_fd = None

def setup_terminal():
    global _unix_old_settings, _unix_fd
    if not _is_windows:
        import termios
        import tty
        _unix_fd = sys.stdin.fileno()
        _unix_old_settings = termios.tcgetattr(_unix_fd)
        tty.setcbreak(_unix_fd)

def restore_terminal():
    if not _is_windows and _unix_old_settings:
        import termios
        termios.tcsetattr(_unix_fd, termios.TCSADRAIN, _unix_old_settings)

def get_key():
    if _is_windows:
        import msvcrt
        if not msvcrt.kbhit():
            return None
        ch = msvcrt.getch()
        if ch == b"\xe0":
            ch2 = msvcrt.getch()
            if ch2 == b"H": return "UP"
            if ch2 == b"P": return "DOWN"
            return None
        if ch == b"\x1b": return "ESC"
        if ch == b" ": return "SPACE"
        try:
            return ch.decode(errors="ignore").lower() or None
        except:
            return None
    else:
        import select
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if not dr:
            return None
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            if seq == "[A": return "UP"
            if seq == "[B": return "DOWN"
            return "ESC"
        if ch == " ": return "SPACE"
        return ch.lower()

def run_intro():
    clear()
    term_w, term_h = get_term_size()

    block_h = len(INTRO_BANNER) + 1
    top_margin = max(0, (term_h - block_h) // 2)

    print("\n" * top_margin)

    for line in INTRO_BANNER:
        padding = max(0, (term_w - len(line)) // 2)
        print(" " * padding + WHITE_ANSI + line + RESET_ANSI)

    prompt_1 = "Press [ENTER] to start"
    padding_1 = max(0, (term_w - len(prompt_1)) // 2)
    print(" " * padding_1 + prompt_1)

    input()

    while True:
        clear()
        term_w, term_h = get_term_size()

        top_margin = max(0, (term_h - block_h) // 2)

        print("\n" * top_margin)

        for line in INTRO_BANNER:
            padding = max(0, (term_w - len(line)) // 2)
            print(" " * padding + WHITE_ANSI + line + RESET_ANSI)

        prompt_2 = "Enter duration (HH:MM:SS or MM:SS): "
        padding_2 = max(0, (term_w - len(prompt_2)) // 2)

        try:
            user_input = input(" " * padding_2 + prompt_2)
        except ValueError:
            continue

        seconds = parse_duration(user_input.strip())
        if seconds is not None and seconds > 0:
            return float(seconds)

        error_msg = "Invalid format. Try 00:05:00"
        err_pad = max(0, (term_w - len(error_msg)) // 2)
        print(f"\n{' ' * err_pad}{RED_ANSI}{error_msg}{RESET_ANSI}")
        time.sleep(1.5)

def clamp_remaining(x, max_s):
    if x < 0: return 0.0
    if x > max_s: return float(max_s)
    return float(x)

def edge_trigger_bucket(prev_seconds, now_seconds, bucket_size):
    if bucket_size <= 0: return False
    return (int(prev_seconds) // bucket_size) != (int(now_seconds) // bucket_size)

def main():
    parser = argparse.ArgumentParser(add_help=False, description=HELP_TEXT, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-d", "--duration", type=str, help="Duration in HH:MM:SS or MM:SS")

    args, unknown = parser.parse_known_args()

    if args.help:
        clear()
        print(HELP_TEXT)
        sys.exit(0)

    total_seconds = 0

    if args.duration:
        total_seconds = parse_duration(args.duration)
        if not total_seconds or total_seconds <= 0:
            print(f"{RED_ANSI}Error: Invalid duration format.{RESET_ANSI}")
            sys.exit(1)
    else:
        try:
            total_seconds = run_intro()
        except KeyboardInterrupt:
            sys.exit(0)

    max_seconds = total_seconds
    remaining = float(total_seconds)
    paused = False

    feedback_until = 0.0
    feedback_color = None

    last_now = time.monotonic()

    setup_terminal()
    clear()

    try:
        while True:
            now = time.monotonic()
            dt_real = now - last_now
            last_now = now

            dt_timer = dt_real * SPEED if SPEED > 0 else 0.0

            key = get_key()
            if key == "UP":
                before = remaining
                remaining = clamp_remaining(remaining + ADJUST_STEP, max_seconds)
                if remaining > before:
                    feedback_color = GREEN_ANSI
                    feedback_until = now + FLASH_FEEDBACK_DURATION
            elif key == "DOWN":
                before = remaining
                remaining = clamp_remaining(remaining - ADJUST_STEP, max_seconds)
                if remaining < before:
                    feedback_color = RED_ANSI
                    feedback_until = now + FLASH_FEEDBACK_DURATION
            elif key == "SPACE":
                paused = not paused
            elif key == "r":
                remaining = max_seconds
                paused = False
            elif key == "ESC":
                break

            prev_remaining = remaining
            if not paused and remaining > 0:
                remaining = clamp_remaining(remaining - dt_timer, max_seconds)

            r_int = int(remaining)

            clear()
            term_w, term_h = get_term_size()

            if paused:
                print_block(center_block(PAUSED_BANNER, term_w, term_h), RED_ANSI)
                time.sleep(0.02)
                continue

            if remaining <= 0:
                print_block(center_block(GAME_OVER, term_w, term_h), RED_ANSI)
                time.sleep(0.02)
                continue

            r = r_int
            h = r // 3600
            m = (r % 3600) // 60
            s = r % 60
            time_str = f"{h:02}:{m:02}:{s:02}"

            color = RESET_ANSI

            if now < feedback_until and feedback_color:
                color = feedback_color

            else:
                if edge_trigger_bucket(int(prev_remaining), r_int, RED_INTERVAL):
                    feedback_color = RED_ANSI
                    feedback_until = now + 1.0
                    color = RED_ANSI

                elif r_int <= FLASH_LAST_SECONDS:
                    if r_int % 2 == 0:
                        color = RED_ANSI
                    else:
                        color = RESET_ANSI

            block = render_time(time_str)
            print_block(center_block(block, term_w, term_h), color)

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        restore_terminal()
        clear()

if __name__ == "__main__":
    main()
