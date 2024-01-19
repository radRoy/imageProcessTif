# This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
window = tk.Tk()
window.wm_attributes('-topmost', 1)
window.withdraw()  # this suppresses the tk window