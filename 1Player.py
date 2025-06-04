import tkinter as tk
import math

# --- Einstellungen zu Beginn ---
gravitation = float(input("Gravitation eingeben (z.B. 9.8): "))
winkel_deg = float(input("Winkel in Grad eingeben (z.B. 45): "))
geschwindigkeit = float(input("Geschwindigkeit eingeben (z.B. 50): "))

# Fenster erstellen
fenster = tk.Tk()
fenster.title("Ballwurf-Spiel")

# Zeichenbereich
breite = 800
hoehe = 400
canvas = tk.Canvas(fenster, width=breite, height=hoehe, bg="white")
canvas.pack()

# Rechteck links (Startspieler)
spieler_rect = canvas.create_rectangle(50, hoehe-100, 100, hoehe-50, fill="blue")

# Ziel-Rechteck rechts
ziel_rect = canvas.create_rectangle(breite-100, hoehe-100, breite-50, hoehe-50, fill="red")

# Punktestand
punkte = 0
punkt_text = canvas.create_text(10, 10, anchor="nw", text="Punkte: 0", font=("Arial", 14), fill="black")

# Ball-Startposition
ball_radius = 5
start_x = 100
start_y = hoehe - 75
ball = canvas.create_oval(start_x-ball_radius, start_y-ball_radius,
                          start_x+ball_radius, start_y+ball_radius, fill="black")

# Geschwindigkeit in x- und y-Richtung berechnen
winkel_rad = math.radians(winkel_deg)
v_x = geschwindigkeit * math.cos(winkel_rad)
v_y = -geschwindigkeit * math.sin(winkel_rad)  # negative y-Richtung ist nach oben

# Zeitvariable
t = 0
dt = 0.1

def bewege_ball():
    global t, punkte

    # Position berechnen
    x = start_x + v_x * t
    y = start_y + v_y * t + 0.5 * gravitation * t**2

    # Ball neu positionieren
    canvas.coords(ball, x - ball_radius, y - ball_radius, x + ball_radius, y + ball_radius)

    # Ziel-Rechteck Position holen
    ziel_coords = canvas.coords(ziel_rect)
    zx1, zy1, zx2, zy2 = ziel_coords

    # Kollision prüfen
    if zx1 < x < zx2 and zy1 < y < zy2:
        punkte += 1
        canvas.itemconfig(punkt_text, text=f"Punkte: {punkte}")
        print("Treffer!")
        return

    # Wenn Ball den Boden berührt -> stoppen
    if y > hoehe:
        print("Verfehlt!")
        return

    # Zeit erhöhen und Funktion erneut aufrufen
    t += dt
    fenster.after(int(dt * 1000), bewege_ball)

# Button zum Starten des Wurfs
start_button = tk.Button(fenster, text="Wurf starten", command=bewege_ball)
start_button.pack()

# Fenster starten
fenster.mainloop()
