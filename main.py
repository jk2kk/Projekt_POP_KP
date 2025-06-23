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

# --- Pracownicy ---
def dodaj_p():
    im, nz, mi, srv = e_imie_p.get().strip(), e_nazw_p.get().strip(), e_miasto_p.get().strip(), e_srv_p.get().strip()
    if not all([im, nz, mi, srv]): return
    lat, lon = get_coords(mi)
    pracownicy.append({'imie': im, 'nazw': nz, 'miasto': mi, 'lat': lat, 'lon': lon, 'do': srv})
    odswiez(l_p, pracownicy, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")
    for e in (e_imie_p, e_nazw_p, e_miasto_p, e_srv_p): e.delete(0, END)

def usun_p():
    idx = l_p.curselection()
    if idx:
        pracownicy.pop(idx[0])
        odswiez(l_p, pracownicy, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")

def akt_p():
    idx = l_p.curselection()
    if not idx: return
    im, nz, mi, srv = e_imie_p.get().strip(), e_nazw_p.get().strip(), e_miasto_p.get().strip(), e_srv_p.get().strip()
    if all([im, nz, mi, srv]):
        lat, lon = get_coords(mi)
        pracownicy[idx[0]].update(imie=im, nazw=nz, miasto=mi, lat=lat, lon=lon, do=srv)
        odswiez(l_p, pracownicy, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")
        for e in (e_imie_p, e_nazw_p, e_miasto_p, e_srv_p): e.delete(0, END)

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
l_s = Listbox(frame, height=3, width=40, font=font_small); l_s.pack(fill=X, pady=3)

Label(frame, text="Pracownik (imię / nazwisko / miasto / serwerownia)", font=font_small).pack(pady=(2, 0))
e_imie_p, e_nazw_p, e_miasto_p, e_srv_p = [Entry(frame, font=font_small) for _ in range(4)]
[e.pack(fill=X) for e in (e_imie_p, e_nazw_p, e_miasto_p, e_srv_p)]
Button(frame, text="Dodaj", command=dodaj_p, font=font_small).pack(fill=X)
Button(frame, text="Usuń", command=usun_p, font=font_small).pack(fill=X)
Button(frame, text="Aktualizuj", command=akt_p, font=font_small).pack(fill=X)
l_p = Listbox(frame, height=3, width=40, font=font_small); l_p.pack(fill=X, pady=3)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=740)
map_widget.pack(side=RIGHT, fill=BOTH, expand=True)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)

root.mainloop()