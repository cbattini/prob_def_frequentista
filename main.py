import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button

'''
Simulazione della definizione frequentista della probabilità in condizione controllate.
Dado a F facce non truccato.
E="esce uno dei numeri in E"
'''

# parametri iniziali
# numero facce
F = 6
# numeri da trovare
E = [3]
# esponente di 10: lanci per realizzazione N = 10**esp
esp = 4
# numero di realizzazioni
R = 10


def aggiorna_caricatore(testo, msg):
    testo.set_text(msg)
    fig.canvas.draw()
    fig.canvas.flush_events()


def simula(F, E, N, R, testo):
    risultati = {}
    for j in range(1, R+1, 1):
        n=0
        frequenze=[]
        for i in range(1, N+1, 1):
            faccia=np.random.randint(1, F+1)
            if(faccia in E):
                n+=1
            frequenze.append(n / i)
        risultati[f"R{j}"] = {
            "N": list(range(1, N+1)),
            "n/N": frequenze,
        }
        aggiorna_caricatore(testo, f"Caricamento... {j}/{R} ({100*j//R}%)")
    return risultati


def disegna(F, E, esp, R):
    N = 10**esp

    # caricatore
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    testo = ax.text(0.5, 0.5, "", ha="center", va="center", fontsize=14, transform=ax.transAxes)
    aggiorna_caricatore(testo, f"Caricamento... 0/{R} (0%)")

    risultati = simula(F, E, N, R, testo)
    P = len(E)/F
    print("P(E): ", round(P, 3))

    ax.clear()

    # Plot P(E)
    ax.axhline(P, color="r", linestyle="--")

    # Plot def. frequentista
    for d in risultati.values():
        ax.plot(d["N"], d["n/N"], color="k", linewidth=0.8)

    ax.set_xscale("log")
    ax.set_xlim(1, N)
    ax.set_ylim(0, 1)
    ax.set_xlabel("N")
    ax.set_ylabel("n/N")
    ax.set_title(f"F={F}, E={E}, N=10^{esp}, R={R}  -  P(E)={round(P, 3)}")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    fig.canvas.draw_idle()


def rigenera(event):
    F = int(box_F.text)
    E = [int(x) for x in box_E.text.split(",")]
    esp = int(box_esp.text)
    R = int(box_R.text)
    disegna(F, E, esp, R)


# Grafico
fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.3)

# caselle per i parametri
box_F = TextBox(plt.axes([0.24, 0.13, 0.12, 0.05]), "F (n. facce) ", initial=str(F))
box_E = TextBox(plt.axes([0.66, 0.13, 0.20, 0.05]), "E (numeri favorevoli) ", initial=",".join(map(str, E)))
box_esp = TextBox(plt.axes([0.24, 0.05, 0.12, 0.05]), "esp (N = 10^esp) ", initial=str(esp))
box_R = TextBox(plt.axes([0.66, 0.05, 0.08, 0.05]), "R (n. realizzazioni) ", initial=str(R))
bottone = Button(plt.axes([0.78, 0.05, 0.08, 0.05]), "Rigenera")
bottone.on_clicked(rigenera)

plt.show(block=False)
disegna(F, E, esp, R)
plt.show()