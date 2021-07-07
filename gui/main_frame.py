import tkinter as tk
from tkinter.ttk import Style


def center_window(w=570, h=287):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    return (w, h, x, y)


def on_closing():
    server_status = func.find_proc_by_name(cfg.tftpd_svc_name)
    if server_status:
        func.tftpd_stop()
    os._exit(0)


root = tk.Tk()
root.title('Cisco Config Manager')
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.geometry('%dx%d+%d+%d' % center_window())


global_style = Style()
global_style.theme_use("default")
global_style.configure("TProgressbar", thickness=8, background='green')


from gui.tftp_frame import *
from gui.cfg_frame import *
from gui.hard_frame import *