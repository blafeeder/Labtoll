
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from FB_verseny import FB_Verseny
import time


verseny = FB_Verseny()


def fb_uj_verseny():
    global verseny

    if not messagebox.askyesno("Új verseny", "Biztosan új versenyt szeretnél kezdeni? Minden adat, ami nem került mentésre törlődni fog!"):
        return

    verseny = FB_Verseny()
    fb_jatekoskezeles_engedelyezese()
    verseny_neve.delete(0, tk.END)
    nev.delete(0, tk.END)
    letszam.set(6)
    lista.delete(0, tk.END)
    fordulo_valaszto.set("")
    fordulo_valaszto["values"] = []

    for widget in keret_merkozesek.winfo_children():
        widget.destroy()

    fb_tabella_megjelenitese()


def fb_jatekoskezeles_tiltasa():
    nev.config(state="disabled")
    gomb_hozzaad.config(state="disabled")
    gomb_torles.config(state="disabled")
    letszam.config(state="disabled")


def fb_jatekoskezeles_engedelyezese():
    nev.config(state="normal")
    gomb_hozzaad.config(state="normal")
    gomb_torles.config(state="normal")
    letszam.config(state="readonly")




def fb_tabella_megjelenitese():
    for sor in tabella.get_children():
        tabella.delete(sor)

    rendezett_tabella = verseny.fb_tabella_rendezese()
    hely = 1

    for jatekos, statisztika in rendezett_tabella:

        if hely == 1:
            szin = "arany"
        elif hely == 2:
            szin = "ezust"
        elif hely == 3:
            szin = "bronz"
        else:
            szin = ""

        tabella.insert("", tk.END, values=(
            hely,
            jatekos,
            statisztika["jatszott"],
            statisztika["gyozelem"],
            statisztika["vereseg"],
            statisztika["nyert_szett"],
            statisztika["vesztett_szett"],
            statisztika["szettkulonbseg"]
        ), tags=(szin,))
        hely += 1



def fb_eredmeny_valtozas(event):
    eredmeny_valaszto = event.widget
    verseny.fb_eredmeny_rogzitese(eredmeny_valaszto.meccs, eredmeny_valaszto.get())
    fb_tabella_megjelenitese()



def fb_merkozesek_megjelenitese(event=None):
    for widget in keret_merkozesek.winfo_children():
        widget.destroy()

    index = 0
    for meccs in verseny.merkozesek:
        if meccs["fordulo"] == int(fordulo_valaszto.get()):
            felirat = ttk.Label(keret_merkozesek, text=f"{meccs['jatekos1']} - {meccs['jatekos2']}")
            felirat.grid(row=index, column=0, padx=10, pady=5, sticky="w")
            eredmeny_valaszto = ttk.Combobox(keret_merkozesek, values=["Nincs eredmény", "2-0", "0-2", "2-1", "1-2"], state="readonly", width=15)

            if meccs["eredmeny"] is None:
                eredmeny_valaszto.set("Nincs eredmény")
            else:
                eredmeny_valaszto.set(meccs["eredmeny"])

            eredmeny_valaszto.grid(row=index, column=1, padx=10, pady=5)
            eredmeny_valaszto.meccs = meccs
            eredmeny_valaszto.bind("<<ComboboxSelected>>", fb_eredmeny_valtozas)
            index += 1


def fb_betoltes():
    fajlnev = filedialog.askopenfilename(filetypes=[("JSON fájl", "*.json")])

    if fajlnev:
        try:
            verseny.fb_betoltes(fajlnev)
            verseny_neve.delete(0, tk.END)
            verseny_neve.insert(0, verseny.nev)
            letszam.set(verseny.csoportletszam)
            lista.delete(0, tk.END)

            for jatekos in verseny.jatekosok:
                lista.insert(tk.END, jatekos)

            fordulo_valaszto["values"] = list(range(1, verseny.fordulok_szama + 1))

            if verseny.fordulok_szama > 0:
                fordulo_valaszto.current(0)
                fb_merkozesek_megjelenitese()
                fb_jatekoskezeles_tiltasa()
            else:
                fordulo_valaszto.set("")

                for widget in keret_merkozesek.winfo_children():
                    widget.destroy()

                fb_jatekoskezeles_engedelyezese()
            fb_tabella_megjelenitese()
            messagebox.showinfo("Betöltés", "Sikeres betöltés!")

        except (OSError, ValueError, KeyError):
            messagebox.showerror("Hiba", "Sikertelen betöltés!")


def fb_mentes():
    fajlnev = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON fájl", "*.json")])

    if fajlnev:
        verseny.nev = verseny_neve.get()
        verseny.csoportletszam = int(letszam.get())

        try:
            verseny.fb_mentes(fajlnev)
            messagebox.showinfo("Mentés", "Sikeres mentés!")
        except OSError:
            messagebox.showerror("Hiba", "Sikertelen mentés!")



def fb_sorsolas():
    verseny.csoportletszam = int(letszam.get())

    if len(verseny.jatekosok) != verseny.csoportletszam:
        messagebox.showwarning("Figyelmeztetés","A játékosok száma nem egyezik meg!")
        return

    verseny.nev = verseny_neve.get()
    kezdes = time.time()
    verseny.fb_sorsolas()
    ido = time.time() - kezdes
    datum = time.strftime("%Y.%m.%d. %H:%M:%S", time.localtime())
    fordulo_valaszto["values"] = list(range(1, verseny.fordulok_szama + 1))
    fordulo_valaszto.current(0)
    fb_merkozesek_megjelenitese()
    fb_tabella_megjelenitese()
    fb_jatekoskezeles_tiltasa()
    messagebox.showinfo("Sikeres sorsolás", f"Sorsolás időpontja: {datum}\nFutási idő: {ido:.6f} mp")

def fb_hozzaad():
    jatekos = nev.get().strip()
    verseny.csoportletszam = int(letszam.get())

    if jatekos == "":
        messagebox.showwarning("Figyelmeztetés", "Nem megfelelő a játékosnév!")

    elif not verseny.fb_van_szabad_hely():
        messagebox.showwarning("Figyelmeztetés", "A csoport már megtelt!")

    elif verseny.fb_jatekos_letezik(jatekos):
        messagebox.showwarning("Figyelmeztetés", "Ez a játékos már szerepel a listában!")

    else:
        verseny.fb_jatekos_hozzaadasa(jatekos)
        lista.insert(tk.END, jatekos)
        nev.delete(0, tk.END)




def fb_torles():
    kijelolt = lista.curselection()

    if kijelolt:
        verseny.fb_jatekos_torlese(kijelolt[0])
        lista.delete(kijelolt[0])
    else:
        messagebox.showwarning("Figyelmeztetés", "Nem jelöltél ki játékost!")


foablak = tk.Tk()
foablak.title("Lábtoll-labda sorsoló")
foablak.geometry("1200x920")


keret_verseny = ttk.LabelFrame(foablak, text="Verseny adatai")
keret_verseny.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

felirat_verseny = ttk.Label(keret_verseny, text="Verseny neve:")
felirat_verseny.grid(row=0, column=0, padx=10, pady=10, sticky="w")

verseny_neve = ttk.Entry(keret_verseny, width=40)
verseny_neve.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

felirat_csop = ttk.Label(keret_verseny, text="Csoportlétszám:")
felirat_csop.grid(row=0, column=2, padx=10, pady=10, sticky="w")

letszam = ttk.Combobox(keret_verseny, values=list(range(2, 17)),
                       state="readonly", width=10)
letszam.grid(row=0, column=3, padx=10, pady=10, sticky="w")
letszam.set(6)

keret_verseny.columnconfigure(1, weight=1)



keret_jatekosok = ttk.LabelFrame(foablak, text="Játékosok kezelése")
keret_jatekosok.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

felirat_jatekosok = ttk.Label(keret_jatekosok, text="Játékos neve:")
felirat_jatekosok.grid(row=0, column=0, padx=10, pady=5, sticky="w")

nev = ttk.Entry(keret_jatekosok, width=28)
nev.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

gomb_hozzaad = ttk.Button(keret_jatekosok, text="Hozzáadás", command=fb_hozzaad)
gomb_hozzaad.grid(row=0, column=2, padx=10, pady=5, sticky="w")

gomb_torles = ttk.Button(keret_jatekosok, text="Törlés", command=fb_torles)
gomb_torles.grid(row=0, column=3, padx=10, pady=5, sticky="w")

felirat_lista = ttk.Label(keret_jatekosok, text="Játékosok listája:")
felirat_lista.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

lista = tk.Listbox(keret_jatekosok, height=16)
lista.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

keret_jatekosok.columnconfigure(0, weight=1)
keret_jatekosok.columnconfigure(1, weight=1)
keret_jatekosok.rowconfigure(4, weight=1)



keret_fordulo = ttk.LabelFrame(foablak, text="Mérkőzések")
keret_fordulo.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

felirat_merkozesek = ttk.Label(keret_fordulo, text="Forduló:")
felirat_merkozesek.grid(row=0, column=0, padx=10, pady=10, sticky="w")

fordulo_valaszto = ttk.Combobox(keret_fordulo, state="readonly", width=15)
fordulo_valaszto.grid(row=0, column=1, padx=10, pady=10, sticky="w")
fordulo_valaszto.bind("<<ComboboxSelected>>", fb_merkozesek_megjelenitese)

keret_merkozesek = ttk.Frame(keret_fordulo)
keret_merkozesek.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nw")



keret_tabella = ttk.LabelFrame(foablak, text="Aktuális tabella")
keret_tabella.grid(row=2, column=0, columnspan=2,
                  padx=10, pady=5, sticky="nsew")

tabella = ttk.Treeview(keret_tabella, columns=("hely", "jatekos", "m", "gy", "v", "ny", "vs", "kul"), show="headings", height=16)

tabella.heading("hely", text="Hely")
tabella.heading("jatekos", text="Játékos")
tabella.heading("m", text="M")
tabella.heading("gy", text="Gy")
tabella.heading("v", text="V")
tabella.heading("ny", text="Ny. sz.")
tabella.heading("vs", text="V. sz.")
tabella.heading("kul", text="Kül.")

tabella.column("hely", width=60, anchor="center", stretch=False)
tabella.column("jatekos", width=250, anchor="w")
tabella.column("m", width=70, anchor="center")
tabella.column("gy", width=70, anchor="center")
tabella.column("v", width=70, anchor="center")
tabella.column("ny", width=90, anchor="center")
tabella.column("vs", width=90, anchor="center")
tabella.column("kul", width=90, anchor="center")

tabella.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

tabella.tag_configure("arany", background="#FFD700", foreground="black")
tabella.tag_configure("ezust", background="#C0C0C0", foreground="black")
tabella.tag_configure("bronz", background="#CD7F32", foreground="black")

keret_tabella.columnconfigure(0, weight=1)
keret_tabella.rowconfigure(0, weight=1)




keret_muveletek = ttk.LabelFrame(foablak, text="Versenyműveletek")
keret_muveletek.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

gomb_sorsolas = ttk.Button(keret_muveletek, text="Sorsolás", command=fb_sorsolas)
gomb_sorsolas.grid(row=0, column=0, padx=10, pady=10, sticky="w")

gomb_mentes = ttk.Button(keret_muveletek, text="Verseny mentése", command=fb_mentes)
gomb_mentes.grid(row=0, column=1, padx=10, pady=10, sticky="w")

gomb_betoltes = ttk.Button(keret_muveletek, text="Verseny betöltése", command=fb_betoltes)
gomb_betoltes.grid(row=0, column=2, padx=10, pady=10, sticky="w")

gomb_uj_verseny = ttk.Button(keret_muveletek, text="Új verseny", command=fb_uj_verseny)
gomb_uj_verseny.grid(row=0, column=3, padx=10, pady=10, sticky="w")


foablak.columnconfigure(0, weight=1)
foablak.columnconfigure(1, weight=2)

foablak.rowconfigure(1, weight=1)
foablak.rowconfigure(2, weight=1)

foablak.mainloop()
