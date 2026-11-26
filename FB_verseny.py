import json

class FB_Verseny:
    def __init__(self):
        self.nev = ""
        self.jatekosok = []
        self.merkozesek = []
        self.fordulok_szama = 0
        self.csoportletszam = 6


    def fb_tabella_rendezese(self):
        statisztika = self.fb_tabella_szamitas()

        rendezett_tabella = sorted(
            statisztika.items(),
            key=lambda jatekos: (
                jatekos[1]["gyozelem"],
                jatekos[1]["szettkulonbseg"],
                jatekos[1]["nyert_szett"]
            ),
            reverse=True
        )
        return rendezett_tabella


    def fb_tabella_szamitas(self):
        statisztika = {}

        for jatekos in self.jatekosok:
            statisztika[jatekos] = {
                "jatszott": 0,
                "gyozelem": 0,
                "vereseg": 0,
                "nyert_szett": 0,
                "vesztett_szett": 0,
                "szettkulonbseg": 0
            }
        for meccs in self.merkozesek:
            if meccs["eredmeny"] is not None:
                jatekos1 = meccs["jatekos1"]
                jatekos2 = meccs["jatekos2"]

                szett1, szett2 = meccs["eredmeny"].split("-")
                szett1 = int(szett1)
                szett2 = int(szett2)

                statisztika[jatekos1]["jatszott"] += 1
                statisztika[jatekos2]["jatszott"] += 1
                statisztika[jatekos1]["nyert_szett"] += szett1
                statisztika[jatekos1]["vesztett_szett"] += szett2
                statisztika[jatekos2]["nyert_szett"] += szett2
                statisztika[jatekos2]["vesztett_szett"] += szett1

                if szett1 > szett2:
                    statisztika[jatekos1]["gyozelem"] += 1
                    statisztika[jatekos2]["vereseg"] += 1
                else:
                    statisztika[jatekos2]["gyozelem"] += 1
                    statisztika[jatekos1]["vereseg"] += 1

        for jatekos in statisztika:
            statisztika[jatekos]["szettkulonbseg"] = (statisztika[jatekos]["nyert_szett"] - statisztika[jatekos]["vesztett_szett"])
        return statisztika


    def fb_eredmeny_rogzitese(self, meccs, eredmeny):
        if eredmeny == "Nincs eredmény":
            meccs["eredmeny"] = None
        else:
            meccs["eredmeny"] = eredmeny

    def fb_van_szabad_hely(self):
        return len(self.jatekosok) < self.csoportletszam


    def fb_jatekos_letezik(self, jatekos):
        return jatekos in self.jatekosok


    def fb_jatekos_hozzaadasa(self, jatekos):
        self.jatekosok.append(jatekos)


    def fb_jatekos_torlese(self, index):
        self.jatekosok.pop(index)


    def fb_sorsolas(self):
        self.merkozesek.clear()
        temp_jatekosok = self.jatekosok.copy()

        if len(temp_jatekosok) % 2 != 0:
            temp_jatekosok.append("Pihenő")

        oletszam = len(temp_jatekosok)
        self.fordulok_szama = oletszam - 1

        for fordulo in range(self.fordulok_szama):
            for i in range(oletszam // 2):
                jatekos1 = temp_jatekosok[i]
                jatekos2 = temp_jatekosok[oletszam - 1 - i]

                if jatekos1 != "Pihenő" and jatekos2 != "Pihenő":
                    self.merkozesek.append({
                        "fordulo": fordulo + 1,
                        "jatekos1": jatekos1,
                        "jatekos2": jatekos2,
                        "eredmeny": None
                    })

            temp_jatekosok = [temp_jatekosok[0]] + [temp_jatekosok[-1]] + temp_jatekosok[1:-1]




    def fb_mentes(self, fajlnev):
        adatok = {
            "nev": self.nev,
            "csoportletszam": self.csoportletszam,
            "jatekosok": self.jatekosok,
            "merkozesek": self.merkozesek,
            "fordulok_szama": self.fordulok_szama
        }

        with open(fajlnev, "w", encoding="utf-8") as fajl:
            json.dump(adatok, fajl, ensure_ascii=False, indent=4)



    def fb_betoltes(self, fajlnev):
        with open(fajlnev, "r", encoding="utf-8") as fajl:
            adatok = json.load(fajl)

        self.nev = adatok["nev"]
        self.csoportletszam = adatok["csoportletszam"]
        self.jatekosok = adatok["jatekosok"]
        self.merkozesek = adatok["merkozesek"]
        self.fordulok_szama = adatok["fordulok_szama"]