# Lábtoll-labda sorsoló és versenykezelő

## Név: Földi Béla

## A feladat leírása

A program célja 2–16 játékos részvételével zajló lábtoll-labda körmérkőzéses verseny lebonyolításának támogatása. Minden játékos egyszer játszik minden másik játékossal. Páratlan létszám esetén fordulónként egy játékos pihen. A párosítások forgatásos módszerrel, a játékosok felvételi sorrendje alapján készülnek.

A program lehetőséget biztosít a verseny nevének és a csoportlétszámnak a megadására, a játékosok felvételére és törlésére, a mérkőzések párosítására, az eredmények rögzítésére, valamint a tabella automatikus kiszámítására és rendezésére. Az első három helyezett arany, ezüst és bronz színnel jelenik meg.

A sorsolás után a játékosok felvétele, törlése és a csoportlétszám módosítása letiltásra kerül. A verseny adatai JSON-fájlba menthetők és később visszatölthetők. Az Új verseny gombbal megerősítés után új, üres verseny indítható.

Sikeres sorsolás után a program megjeleníti a sorsolás időpontját és az algoritmus futási idejét.

A tabella rendezési szempontjai sorrendben: győzelmek száma, szettkülönbség, nyert szettek száma. Teljes egyezés esetén az eredeti játékossorrend marad meg.

A mérkőzések választható eredményei: `2-0`, `0-2`, `2-1`, `1-2`. A „Nincs eredmény” kiválasztásával a korábban rögzített eredmény visszavonható.

A tabella oszlopai: helyezés, játékos neve, lejátszott mérkőzések (M), győzelmek (Gy), vereségek (V), nyert szettek (Ny. sz.), vesztett szettek (V. sz.) és szettkülönbség (Kül.).

## Felhasznált modulok

### Tanult modulok

| Modul | Használt függvények, osztályok | Feladat |
| --- | --- | --- |
| `tkinter` | `Tk()`, `Listbox()` | Grafikus felület |
| `tkinter.ttk` | `Label()`, `Entry()`, `Combobox()`, `Button()`, `Frame()`, `LabelFrame()`, `Treeview()` | Grafikus vezérlőelemek |
| `tkinter.messagebox` | `showinfo()`, `showwarning()`, `showerror()`, `askyesno()` | Üzenetek és megerősítő párbeszédablak |
| `tkinter.filedialog` | `asksaveasfilename()`, `askopenfilename()` | Fájl kiválasztása mentéshez és betöltéshez |
| `json` | `dump()`, `load()` | Versenyadatok mentése és betöltése |

### Bemutatandó modul: `time`

A Python beépített `time` modulja a sorsolási algoritmus futási idejének mérésére és a sorsolás időpontjának megjelenítésére szolgál. A főprogram `fb_sorsolas()` függvényében három különböző modulfüggvény szerepel.

| Függvény | Feladat |
| --- | --- |
| `time.time()` | Az aktuális időbélyeg lekérése a sorsolás előtt és után; a különbség a futási idő másodpercben. |
| `time.localtime()` | Az aktuális helyi idő lekérése. |
| `time.strftime()` | A helyi idő formázása év, hónap, nap, óra, perc és másodperc szerint. |

A sikeres sorsolás után egy párbeszédablak jeleníti meg a sorsolás időpontját és az algoritmus futási idejét hat tizedesjegy pontosságú kijelzéssel.

### Saját modul

`FB_verseny.py` – a verseny adatainak és működési logikájának kezelése.

## Saját osztály

### `FB_Verseny`

Az osztály tárolja a verseny nevét, a csoportlétszámot, a játékosokat, a mérkőzéseket és a fordulók számát.

| Metódus | Feladat |
| --- | --- |
| `__init__()` | Kezdeti értékek beállítása |
| `fb_van_szabad_hely()` | Szabad hely ellenőrzése |
| `fb_jatekos_letezik()` | Játékosnév ellenőrzése |
| `fb_jatekos_hozzaadasa()` | Játékos hozzáadása |
| `fb_jatekos_torlese()` | Játékos törlése |
| `fb_sorsolas()` | Körmérkőzéses párosítások elkészítése forgatásos módszerrel |
| `fb_eredmeny_rogzitese()` | Mérkőzéseredmény rögzítése vagy visszavonása |
| `fb_tabella_szamitas()` | Játékosok statisztikáinak kiszámítása |
| `fb_tabella_rendezese()` | Tabella rendezése lambda függvény segítségével |
| `fb_mentes()` | Verseny mentése JSON-fájlba |
| `fb_betoltes()` | Verseny betöltése JSON-fájlból |

## A főprogram saját függvényei

| Függvény | Feladat |
| --- | --- |
| `fb_hozzaad()` | Játékos felvétele a grafikus felületen |
| `fb_torles()` | Kijelölt játékos törlése |
| `fb_sorsolas()` | Sorsolás indítása, futási idő mérése, a felület frissítése és az időadatok megjelenítése |
| `fb_merkozesek_megjelenitese()` | Kiválasztott forduló mérkőzéseinek megjelenítése |
| `fb_eredmeny_valtozas()` | Eredményváltozás kezelése |
| `fb_tabella_megjelenitese()` | Tabella megjelenítése és színezése |
| `fb_mentes()` | Mentési párbeszédablak kezelése |
| `fb_betoltes()` | Betöltési párbeszédablak kezelése és a felület frissítése |
| `fb_jatekoskezeles_tiltasa()` | Játékosfelvétel, törlés és létszámválasztás letiltása |
| `fb_jatekoskezeles_engedelyezese()` | Játékoskezelés újbóli engedélyezése |
| `fb_uj_verseny()` | Megerősítés után új versenyobjektum létrehozása és a felület alaphelyzetbe állítása |

## Eseménykezelés

A nyomógombok eseménykezelése a `command` paraméterrel, a forduló- és eredményválasztó legördülő listák eseményeinek kezelése a `bind()` metódussal és a `<<ComboboxSelected>>` eseménnyel történik. Az eredmény módosításakor a tabella automatikusan frissül.

## A program indítása

A futtatáshoz Python 3 és Tkinter szükséges. Külső Python-csomag telepítése nem szükséges, amennyiben a Tkinter rendelkezésre áll. A `main.py` és az `FB_verseny.py` fájl ugyanabban a könyvtárban legyen.

Indítás parancssorból:

```bash
python main.py
```

## A program használata

1. Adjuk meg a verseny nevét és a csoportlétszámot (2–16 fő, alapértelmezetten 6 fő).
2. Vegyük fel a játékosokat. A „Pihenő” nevet ne használjuk játékosnévként, mert azt a sorsolási algoritmus használja.
3. A **Sorsolás** gombbal készítsük el a párosításokat. A játékoskezelés ekkor letiltásra kerül, és egy üzenetablakban megjelenik a sorsolás időpontja és futási ideje.
4. Válasszuk ki a fordulót, majd adjuk meg a mérkőzések eredményeit.
5. Kövessük az automatikusan frissülő tabellát.
6. Szükség esetén mentsük a versenyt a **Verseny mentése** gombbal, vagy töltsünk be egy korábban mentett versenyt a **Verseny betöltése** gombbal.
7. Új verseny indításához kattintsunk az **Új verseny** gombra, majd erősítsük meg a műveletet. A felület kiürül, a csoportlétszám visszaáll 6-ra, és a játékoskezelés újra elérhető lesz.

**Figyelem:** az újrasorsolás törli a korábbi mérkőzéseredményeket. Új verseny indítása vagy másik verseny betöltése előtt mentsük el a megtartani kívánt adatokat.
