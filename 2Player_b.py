import tkinter as tk
import math

# Fenster und Zeichenfläche (Canvas)
fenster = tk.Tk()
fenster.title("Ballwurf-Spiel (2 Spieler)")
breite = 800
hoehe = 400
canvas = tk.Canvas(fenster, width=breite, height=hoehe, bg="white")
canvas.grid(row=0, column=0, columnspan=6)

# Zwei Rechtecke für Spieler
spieler1 = canvas.create_rectangle(50, hoehe-100, 100, hoehe-50, fill="blue")
spieler2 = canvas.create_rectangle(breite-100, hoehe-100, breite-50, hoehe-50, fill="red")

# Eingabefelder für Gravitation, Winkel, Geschwindigkeit
tk.Label(fenster, text="Gravitation").grid(row=1, column=0)
entry_grav = tk.Entry(fenster)
entry_grav.insert(0, "9.8")  # Standardwert
entry_grav.grid(row=1, column=1)

tk.Label(fenster, text="Winkel").grid(row=1, column=2)
entry_winkel = tk.Entry(fenster)
entry_winkel.insert(0, "45")  # Standardwert
entry_winkel.grid(row=1, column=3)

tk.Label(fenster, text="Geschwindigkeit").grid(row=1, column=4)
entry_speed = tk.Entry(fenster)
entry_speed.insert(0, "50")  # Standardwert
entry_speed.grid(row=1, column=5)

# Punktestand und Spieleranzeige
punkte1 = 0
punkte2 = 0
aktueller_spieler = [1]  # 1 = Spieler 1, 2 = Spieler 2

anzeige = canvas.create_text(10, 10, anchor="nw",
                             text="Punkte S1: 0 | S2: 0 | Spieler: 1",
                             font=("Arial", 14))

# Aktualisiert die Punkteanzeige im Fenster
def update_anzeige():
    canvas.itemconfig(anzeige, text=f"Punkte S1: {punkte1} | S2: {punkte2} | Spieler: {aktueller_spieler[0]}")

# Startet einen Wurf, liest Parameter aus und berechnet Startposition
def starte_wurf():
    try:
        g = float(entry_grav.get())
        winkel = float(entry_winkel.get())
        v = float(entry_speed.get())
    except:
        return  # Falls Eingaben ungültig sind

    # Startposition & Richtung je nach Spieler
    if aktueller_spieler[0] == 1:
        richtung = 1
        start_x = 100
    else:
        richtung = -1
        start_x = breite - 100

    start_y = hoehe - 75  # gleicher Y-Startpunkt für beide

    # Berechnung der x- und y-Geschwindigkeit aus Winkel & Geschwindigkeit
    winkel_rad = math.radians(winkel)
    vx = v * math.cos(winkel_rad) * richtung
    vy = -v * math.sin(winkel_rad)

    # Ball erzeugen
    ball = canvas.create_oval(start_x-5, start_y-5, start_x+5, start_y+5, fill="black")
    
    # Bewegung starten
    bewege_ball(ball, 0, start_x, start_y, vx, vy, g)

# Animiert den Ball während des Flugs
def bewege_ball(ball, t, x0, y0, vx, vy, g):
    # Neue Position berechnen
    x = x0 + vx * t
    y = y0 + vy * t + 0.5 * g * t * t

    # Ballposition auf Canvas aktualisieren
    canvas.coords(ball, x-5, y-5, x+5, y+5)

    # Zielrechteck je nach Spieler
    if aktueller_spieler[0] == 1:
        ziel = canvas.coords(spieler2)
    else:
        ziel = canvas.coords(spieler1)

    zx1, zy1, zx2, zy2 = ziel

    # Trefferüberprüfung
    if zx1 < x < zx2 and zy1 < y < zy2:
        if aktueller_spieler[0] == 1:
            global punkte1
            punkte1 += 1
        else:
            global punkte2
            punkte2 += 1

        # Spielerwechsel nach Treffer
        if aktueller_spieler[0] == 1:
            aktueller_spieler[0] = 2
        else:
            aktueller_spieler[0] = 1

        update_anzeige()
        return

    # Wenn der Ball den Boden berührt, Spieler wechseln
    if y > hoehe:
        if aktueller_spieler[0] == 1:
            aktueller_spieler[0] = 2
        else:
            aktueller_spieler[0] = 1

        update_anzeige()
        return

    # Weiter bewegen (nur wenn Fenster noch offen)
    if fenster.winfo_exists():
        fenster.after(20, lambda: bewege_ball(ball, t+0.1, x0, y0, vx, vy, g))

# Button zum Starten des Wurfs
tk.Button(fenster, text="Wurf starten", command=starte_wurf).grid(row=2, column=0, columnspan=6)

fenster.mainloop()
