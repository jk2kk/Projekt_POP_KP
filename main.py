

from tkinter import *
import tkintermapview, requests
from bs4 import BeautifulSoup

# --- Lokalizacja ---
def get_coords(city):
    try:
        s = BeautifulSoup(requests.get(f"https://pl.wikipedia.org/wiki/{city}").text, 'html.parser')
        return float(s.select('.latitude')[1].text.replace(',', '.')), float(s.select('.longitude')[1].text.replace(',', '.'))
    except:
        return 52.23, 21.01

serwerownie, pracownicy, klienci = [], [], []

# --- Aktualizacja listboxa ---
def odswiez(box, data, fmt):
    box.delete(0, END)
    for o in data:
        box.insert(END, fmt(o))

# --- Serwerownie ---
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

# --- Klienci ---
def dodaj_k():
    im, nz, mi, srv = e_imie_k.get().strip(), e_nazw_k.get().strip(), e_miasto_k.get().strip(), e_srv_k.get().strip()
    if not all([im, nz, mi, srv]): return
    lat, lon = get_coords(mi)
    klienci.append({'imie': im, 'nazw': nz, 'miasto': mi, 'lat': lat, 'lon': lon, 'do': srv})
    odswiez(l_k, klienci, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")
    for e in (e_imie_k, e_nazw_k, e_miasto_k, e_srv_k): e.delete(0, END)

def usun_k():
    idx = l_k.curselection()
    if idx:
        klienci.pop(idx[0])
        odswiez(l_k, klienci, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")

def akt_k():
    idx = l_k.curselection()
    if not idx: return
    im, nz, mi, srv = e_imie_k.get().strip(), e_nazw_k.get().strip(), e_miasto_k.get().strip(), e_srv_k.get().strip()
    if all([im, nz, mi, srv]):
        lat, lon = get_coords(mi)
        klienci[idx[0]].update(imie=im, nazw=nz, miasto=mi, lat=lat, lon=lon, do=srv)
        odswiez(l_k, klienci, lambda o: f"{o['imie']} {o['nazw']} → {o['do']}")
        for e in (e_imie_k, e_nazw_k, e_miasto_k, e_srv_k): e.delete(0, END)

# --- Mapy ---
def mapa(zrodlo):
    map_widget.delete_all_marker()
    for o in zrodlo:
        if 'lat' in o and 'lon' in o:
            tekst = o.get('nazwa') or f"{o['imie']} {o['nazw']}"
            map_widget.set_marker(o['lat'], o['lon'], text=tekst)
    if zrodlo:
        map_widget.set_position(zrodlo[0]['lat'], zrodlo[0]['lon'])
        map_widget.set_zoom(6)

def mapa_combo():
    idx = l_s.curselection()
    if not idx: return
    srv = serwerownie[idx[0]]
    nazwa = srv['nazwa']
    zbior = [srv] + [o for o in pracownicy + klienci if o['do'] == nazwa]
    mapa(zbior)

def mapa_prac_serw():
    idx = l_s.curselection()
    if not idx: return
    nazwa = serwerownie[idx[0]]['nazwa']
    mapa([o for o in pracownicy if o['do'] == nazwa])

def mapa_klient_serw():
    idx = l_s.curselection()
    if not idx: return
    nazwa = serwerownie[idx[0]]['nazwa']
    mapa([o for o in klienci if o['do'] == nazwa])

# --- GUI ---
root = Tk(); root.title("System serwerowni"); root.geometry("1150x750")
frame = Frame(root); frame.pack(side=LEFT, fill=Y, padx=8, pady=5)
font_small = ('Arial', 8)

# --- Serwerownie ---
Label(frame, text="Serwerownia (nazwa / miasto)", font=font_small).pack(pady=(2, 0))
e_nazwa_s, e_miasto_s = Entry(frame, font=font_small), Entry(frame, font=font_small)
e_nazwa_s.pack(fill=X); e_miasto_s.pack(fill=X)
Button(frame, text="Dodaj", command=dodaj_s, font=font_small).pack(fill=X)
Button(frame, text="Usuń", command=usun_s, font=font_small).pack(fill=X)
Button(frame, text="Aktualizuj", command=akt_s, font=font_small).pack(fill=X)
l_s = Listbox(frame, height=3, width=40, font=font_small); l_s.pack(fill=X, pady=3)

# --- Pracownicy ---
Label(frame, text="Pracownik (imię / nazwisko / miasto / serwerownia)", font=font_small).pack(pady=(2, 0))
e_imie_p, e_nazw_p, e_miasto_p, e_srv_p = [Entry(frame, font=font_small) for _ in range(4)]
[e.pack(fill=X) for e in (e_imie_p, e_nazw_p, e_miasto_p, e_srv_p)]
Button(frame, text="Dodaj", command=dodaj_p, font=font_small).pack(fill=X)
Button(frame, text="Usuń", command=usun_p, font=font_small).pack(fill=X)
Button(frame, text="Aktualizuj", command=akt_p, font=font_small).pack(fill=X)
l_p = Listbox(frame, height=3, width=40, font=font_small); l_p.pack(fill=X, pady=3)

# --- Klienci ---
Label(frame, text="Klient (imię / nazwisko / miasto / serwerownia)", font=font_small).pack(pady=(2, 0))
e_imie_k, e_nazw_k, e_miasto_k, e_srv_k = [Entry(frame, font=font_small) for _ in range(4)]
[e.pack(fill=X) for e in (e_imie_k, e_nazw_k, e_miasto_k, e_srv_k)]
Button(frame, text="Dodaj", command=dodaj_k, font=font_small).pack(fill=X)
Button(frame, text="Usuń", command=usun_k, font=font_small).pack(fill=X)
Button(frame, text="Aktualizuj", command=akt_k, font=font_small).pack(fill=X)
l_k = Listbox(frame, height=3, width=40, font=font_small); l_k.pack(fill=X, pady=3)

# --- Mapy ---
Label(frame, text="Mapy", font=font_small).pack(pady=(5, 0))
Button(frame, text="Mapa wszystkich serwerowni", command=lambda: mapa(serwerownie), font=font_small).pack(fill=X, pady=1)
Button(frame, text="Mapa wszystkich pracowników", command=lambda: mapa(pracownicy), font=font_small).pack(fill=X, pady=1)
Button(frame, text="Mapa wszystkich klientów", command=lambda: mapa(klienci), font=font_small).pack(fill=X, pady=1)
Button(frame, text="Klienci wybranej serwerowni", command=mapa_klient_serw, font=font_small).pack(fill=X, pady=1)
Button(frame, text="Pracownicy wybranej serwerowni", command=mapa_prac_serw, font=font_small).pack(fill=X, pady=1)
Button(frame, text="Serwerownia + podlegli", command=mapa_combo, font=font_small).pack(fill=X, pady=1)
Button(frame, text="🗑 Usuń pinezki", command=lambda: map_widget.delete_all_marker(), font=font_small).pack(fill=X, pady=4)

# --- Mapa ---
map_widget = tkintermapview.TkinterMapView(root, width=800, height=740)
map_widget.pack(side=RIGHT, fill=BOTH, expand=True)
map_widget.set_position(52.23, 21.01); map_widget.set_zoom(6)

root.mainloop()





