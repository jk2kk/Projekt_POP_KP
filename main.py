from tkinter import *
import tkintermapview

serwerownie, pracownicy, klienci = [], [], []

root = Tk()
root.title("System serwerowni")
root.geometry("1150x750")

frame = Frame(root)
frame.pack(side=LEFT, fill=Y, padx=8, pady=5)
font_small = ('Arial', 8)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=740)
map_widget.pack(side=RIGHT, fill=BOTH, expand=True)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)

root.mainloop()