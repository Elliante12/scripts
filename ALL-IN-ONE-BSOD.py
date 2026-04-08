import shutil
import tempfile
import random
import time
import os
import sys
import subprocess
import threading

# -------------------------------
# Temp Relaunch Logic (Fixed)
# -------------------------------

def is_running_from_temp():
    temp_dir = os.path.abspath(tempfile.gettempdir())
    current = os.path.abspath(__file__)
    return os.path.dirname(current).lower() == temp_dir.lower()

if not is_running_from_temp():
    temp_dir = tempfile.gettempdir()
    temp_script = os.path.join(temp_dir, "visual_packet.py")

    try:
        shutil.copy2(__file__, temp_script)
        subprocess.Popen([sys.executable, temp_script])
    except Exception as e:
        print("Failed to relaunch:", e)
        input("Press Enter...")
    
    sys.exit()

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

# -------------------------------
# Main Effect
# -------------------------------

def hack_screen():
    clear()

    type_print(">>> SOMETIMES I DREAM OF SAVING THE WORLD <<<", 0.005)
    print("\n")
    time.sleep(1)

    for _ in range(120):
        print(random_line())
        time.sleep(0.01)

    print("\n")

    type_print(">>> ACCESS GRANTED <<<", 0.03)
    
    print("\n")
    time.sleep(0.2)
    
    for _ in range(random.randint(30, 45)):
        print(f"DATA_PACKET_{random.randint(1000,9999)} :: {random_line(40)}")
        time.sleep(0.02)

    type_print(">>> DOWNLOAD COMPLETE <<<", 0.02)
    type_print(">>> DISCONNECTING <<<", 0.02)
    #threading.Timer(1, lambda: subprocess.run(["shutdown", "/s", "/f", "/t", "0"])).start()

    input("\nPress Enter to exit...")

# -------------------------------
# Run
# -------------------------------

if __name__ == "__main__":
    hack_screen()
