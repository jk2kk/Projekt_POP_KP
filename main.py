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


# --- Lokalizacja ---
def get_coords(city):
    try:
        s = BeautifulSoup(requests.get(f"https://pl.wikipedia.org/wiki/{city}").text, 'html.parser')
        return float(s.select('.latitude')[1].text.replace(',', '.')), float(s.select('.longitude')[1].text.replace(',', '.'))
    except:
        return 52.23, 21.01

serwerownie, pracownicy, klienci = [], [], []

def odswiez(box, data, fmt):
    box.delete(0, END)
    for o in data:
        box.insert(END, fmt(o))

def dodaj_s():
    n, m = e_nazwa_s.get().strip(), e_miasto_s.get().strip()
    if not n or not m: return
    lat, lon = get_coords(m)
    serwerownie.append({'nazwa': n, 'miasto': m, 'lat': lat, 'lon': lon})
    odswiez(l_s, serwerownie, lambda x: f"{x['nazwa']} ({x['miasto']})")
    e_nazwa_s.delete(0, END); e_miasto_s.delete(0, END)

def usun_s():
    idx = l_s.curselection()
    if idx:
        serwerownie.pop(idx[0])
        odswiez(l_s, serwerownie, lambda x: f"{x['nazwa']} ({x['miasto']})")

def akt_s():
    idx = l_s.curselection()
    if not idx: return
    n, m = e_nazwa_s.get().strip(), e_miasto_s.get().strip()
    if n and m:
        lat, lon = get_coords(m)
        serwerownie[idx[0]].update(nazwa=n, miasto=m, lat=lat, lon=lon)
        odswiez(l_s, serwerownie, lambda x: f"{x['nazwa']} ({x['miasto']})")
        e_nazwa_s.delete(0, END); e_miasto_s.delete(0, END)

root = Tk()
root.title("System serwerowni")
root.geometry("1150x750")

frame = Frame(root)
frame.pack(side=LEFT, fill=Y, padx=8, pady=5)
font_small = ('Arial', 8)

Label(frame, text="Serwerownia (nazwa / miasto)", font=font_small).pack(pady=(2, 0))
e_nazwa_s, e_miasto_s = Entry(frame, font=font_small), Entry(frame, font=font_small)
e_nazwa_s.pack(fill=X); e_miasto_s.pack(fill=X)
Button(frame, text="Dodaj", command=dodaj_s, font=font_small).pack(fill=X)
Button(frame, text="Usuń", command=usun_s, font=font_small).pack(fill=X)
Button(frame, text="Aktualizuj", command=akt_s, font=font_small).pack(fill=X)
l_s = Listbox(frame, height=3, width=40, font=font_small)
l_s.pack(fill=X, pady=3)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=740)
map_widget.pack(side=RIGHT, fill=BOTH, expand=True)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)


root.mainloop()