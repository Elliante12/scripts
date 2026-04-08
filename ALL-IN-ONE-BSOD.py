import ctypes
from ctypes import wintypes
import shutil
import tempfile
import random
import time
import os
import sys
import subprocess
import threading

# -------------------------------
# Setup / Relaunch Logic
# -------------------------------

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, 3) 

def is_running_from_temp():
    return tempfile.gettempdir().lower() in os.path.abspath(__file__).lower()

def detect_usb_from_script():
    script_path = os.path.abspath(sys.argv[0])
    drive = os.path.splitdrive(script_path)[0]
    
    if drive:
        return drive.upper()
    
    return None

usb_drive = None

def is_running_from_temp():
    return tempfile.gettempdir().lower() in os.path.abspath(__file__).lower()

usb_drive = None

if not is_running_from_temp():
    # get drive from where script is running (USB)
    usb_drive = os.path.splitdrive(os.path.abspath(__file__))[0]

    if not usb_drive:
        print("Could not detect drive")
        sys.exit()

    temp_dir = tempfile.gettempdir()
    local_script = os.path.join(temp_dir, "malicious_packet_eject.py")

    shutil.copy2(__file__, local_script)

    subprocess.run([sys.executable, local_script, usb_drive])
    sys.exit()

# running from temp
if len(sys.argv) > 1:
    usb_drive = sys.argv[1]

print("USB DRIVE:", usb_drive)

# -------------------------------
# Visual Stuff
# -------------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_line(length=70):
    chars = "1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()_+{}|:?"
    return "".join(random.choice(chars) for _ in range(length))

def type_print(text, delay=0):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    sys.stdout.flush()

def progress_bar(total=30):
    for i in range(total + 1):
        bar = "[" + "#" * i + " " * (total - i) + "]"
        percent = int((i / total) * 100)
        sys.stdout.write(f"\r{bar} {percent}%")
        sys.stdout.flush()
        time.sleep(random.uniform(0.03, 0.06))
    print("\n")

# -------------------------------
# Eject Logic
# -------------------------------

def eject_drive(drive_letter):
    if not drive_letter or ":" not in drive_letter:
        print("Invalid drive:", drive_letter)
        return

    path = f"\\\\.\\{drive_letter}"

    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3

    handle = ctypes.windll.kernel32.CreateFileW(
        path,
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None
    )

    if handle == -1:
        print("Failed to get handle")
        return

    IOCTL_STORAGE_EJECT_MEDIA = 0x2D4808

    bytes_returned = wintypes.DWORD()
    result = ctypes.windll.kernel32.DeviceIoControl(
        handle,
        IOCTL_STORAGE_EJECT_MEDIA,
        None,
        0,
        None,
        0,
        ctypes.byref(bytes_returned),
        None
    )

    ctypes.windll.kernel32.CloseHandle(handle)

    if result:
        print("Ejected successfully")
    else:
        error = ctypes.windll.kernel32.GetLastError()
        print(f"Eject failed, error code: {error}")

# -------------------------------
# Main Effect
# -------------------------------

def hack_screen():
    clear()

    type_print(">>> SOMETIMES I DREAM OF SAVING THE WORLD <<<", 0.005)
    eject_drive(usb_drive)
    time.sleep(2)

    for _ in range(40):
        print(random_line())
        time.sleep(0.01)

    print("\n")

    type_print("\n>>> ACCESS GRANTED <<<", 0.03)

    for _ in range(random.randint(30, 45)):
        print(f"DATA_PACKET_{random.randint(1000,9999)} :: {random_line(40)}")
        time.sleep(0.02)

    type_print("\n>>> DOWNLOAD COMPLETE <<<", 0.02)
    type_print(">>> DISCONNECTING <<<", 0.02)
    #threading.Timer(0.1, lambda: subprocess.run(["shutdown", "/s", "/f", "/t", "0"])).start()

    input("\nPress Enter to exit...")

# -------------------------------
# Run safely
# -------------------------------

if __name__ == "__main__":
    try:
        hack_screen()
    except Exception as e:
        print("\nERROR:", e)
        input("Press Enter to exit...")

