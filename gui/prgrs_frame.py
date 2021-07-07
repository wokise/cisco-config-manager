import tkinter as tk
from tkinter import ttk
import gui.ui_resources as ui


prgrs_frame = tk.Frame()
prgrs_frame.pack(padx=10, side=tk.TOP, fill=tk.BOTH)


pc_lbl = tk.Label(prgrs_frame, image=ui.pc_img)
pc_lbl.pack(side=tk.LEFT, fill=tk.X)

prgrs_bar = ttk.Progressbar(
    prgrs_frame, mode="determinate",
    orient='horizontal', length=116, style="TProgressbar", value=0)
prgrs_bar.pack(padx=10, anchor=tk.CENTER, side=tk.LEFT, fill=tk.X)

swtch_lbl = tk.Label(prgrs_frame, image=ui.switch_img)
swtch_lbl.pack(anchor=tk.E, side=tk.RIGHT)