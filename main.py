import tkinter as tk
from tkinter import ttk
import socket
import platform
import threading
import urllib.request

APP_TITLE = "NETCHECK - Network Checker"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "Tidak diketahui"
    finally:
        s.close()

def check_internet():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=4)
        return True
    except Exception:
        return False

class NetCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("720x540")
        self.root.minsize(600, 450)
        self.root.configure(bg="#eef3f8")