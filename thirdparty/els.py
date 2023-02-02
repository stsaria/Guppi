import ctypes
import os
import platform
import socket
import subprocess
import sys
import time
from threading import Event
import urllib.request

if platform.system() == "Windows":
    ENABLE_PROCESSED_OUTPUT = 0x0001
    ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)
    kernel32.SetConsoleMode(handle, MODE)

    GREEN = "\033[32m"
    RED = '\033[31m'
    Blue = '\033[34m'
    END = '\033[0m'
# 遅延関数化
def wait(time):
    Event().wait(int(time))

def print_els(text_els, print_switch):
    if print_switch == "True":
        print(text_els)
    else:
        pass

def stop_15_sec(print_switch):
    if print_switch == "True":
        wait(15)
        sys.exit()
    else:
        pass

# OS確認
def check_platform(print_switch):
    print_els("Your PC OS [{0}]".format(platform.system()), print_switch)
    return platform.system()

# ファイルチェック（存在）
def check_file_dir(path, error_stop_switch, print_switch):
    is_path_file = os.path.exists(str(path))
    if is_path_file:
        print_els("[OK] File {0}".format(path), print_switch)
        time.sleep(0.5)
        return "ok"
    else:
        print_els("[Error] File {0}".format(path), print_switch)
        if error_stop_switch == "True":
            print_els("Stops the program after 15 seconds", print_switch)
            stop_15_sec(print_switch)
            sys.exit()
        else:
            pass
        return "error"

# Pingで応答来るか
def check_ping(host, count_els):
    error_stop_switch = "False"
    print_switch = "False"
    if not host:
        host = "google.com"
    else:
        pass
    if not count_els:
        count_els = "2"
    else:
        pass
    wait(1)
    if platform.system() == "Windows":
        res = subprocess.run(["ping",host,"-n",count_els, "-w", "300"],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            print_els("[OK] NetWork {0}".format(host), print_switch)
            time.sleep(1.7)
            return True
        else:
            print_els("[Error] Network {0}".format(host), print_switch)
            if error_stop_switch == "True":
                print_els("Stops the program after 15 seconds", print_switch)
                stop_15_sec(print_switch)
                sys.exit()
            return False
    else:
        res = subprocess.run(["ping",host,"-c",count_els],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            print_els("[OK] NetWork {0}".format(host), print_switch)
            time.sleep(1.7)
            return True
        else:
            print_els("[Error] Network {0}".format(host), print_switch)
            if error_stop_switch == "True":
                print_els("Stops the program after 15 seconds", print_switch)
                stop_15_sec(print_switch)
                sys.exit()
            else:
                pass
            return False
# IP確認（192）
def private_ip():
        time.sleep(0.3)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print_els("Private_IP: {0}".format(s.getsockname()[0]), "False")
        time.sleep(1.7)
        return s.getsockname()[0]
# G_IP確認
def global_ip():
    if platform.system() == "Windows":
        res = subprocess.run(["ping","google.com","-n","1", "-w", "300"],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            time.sleep(0.3)
            g_ip = urllib.request.urlopen('http://api.ipify.org/').read().decode('utf-8')
            print_els("Global_IP: {0}".format(g_ip), "False")
            return g_ip, True
        else:
            print_els("[Error] failed to get", "False")
            if "False" == "True":
                print_els("Stops the program after 15 seconds", "False")
                stop_15_sec("False")
                sys.exit()
            return "no", False
