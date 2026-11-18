import os
import sqlite3
from tabulate import tabulate

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials.db")
SEKTOR_AGIRLIKLARI = {
    "automotive": {
        "tensile_strength": 0.20,
        "elastic_modulus": 0.15,
        "density": 0.20,
        "max_temp": 0.10,
        "corrosion_resistance": 0.10,
        "cost": 0.25
    },
    "aerospace": {
        "tensile_strength": 0.25,
        "elastic_modulus": 0.15,
        "density": 0.30,
        "max_temp": 0.15,
        "corrosion_resistance": 0.10,
        "cost": 0.05
    },
    "rail": {
        "tensile_strength": 0.25,
        "elastic_modulus": 0.25,
        "density": 0.05,
        "max_temp": 0.05,
        "corrosion_resistance": 0.15,
        "cost": 0.25
    }
}
def load_materials(db_yolu=DB_PATH):
    if not os.path.exists(db_yolu):
        raise FileNotFoundError("Database file not found.")
    baglanti = sqlite3.connect(db_yolu)
    imlec = baglanti.cursor()
    imlec.execute(
        "SELECT name, category, density, tensile_strength, elastic_modulus, "
        "max_temp, corrosion_resistance, cost FROM materials"
    )
    satirlar = imlec.fetchall()
    baglanti.close()
    liste = []
    for satir in satirlar:
        liste.append({
            "name": satir[0],
            "category": satir[1],
            "density": satir[2],
            "tensile_strength": satir[3],
            "elastic_modulus": satir[4],
            "max_temp": satir[5],
            "corrosion_resistance": satir[6],
            "cost": satir[7]
        })
    return liste
def filter_materials(malzemeler, kosullar):
    uygunlar = []
    elenenler = []
    for eleman in malzemeler:
        nedenler = []
        if kosullar.get("min_tensile") is not None:
            if eleman["tensile_strength"] < kosullar["min_tensile"]:
                nedenler.append("Low tensile strength")
        if kosullar.get("min_modulus") is not None:
            if eleman["elastic_modulus"] < kosullar["min_modulus"]:
                nedenler.append("Low elastic modulus")
        if kosullar.get("min_temp") is not None:
            if eleman["max_temp"] < kosullar["min_temp"]:
                nedenler.append("Low max temp")
        if kosullar.get("max_cost") is not None:
            if eleman["cost"] > kosullar["max_cost"]:
                nedenler.append("Over budget")
        if kosullar.get("min_corrosion") is not None:
            if eleman["corrosion_resistance"] < kosullar["min_corrosion"]:
                nedenler.append("Low corrosion resistance")
        if len(nedenler) == 0:
            uygunlar.append(eleman)
        else:
            elenenler.append({
                "name": eleman["name"],
                "category": eleman["category"],
                "reasons": ", ".join(nedenler)
            })
    return uygunlar, elenenler
def rank_materials(malzemeler, sektor):
    if sektor not in SEKTOR_AGIRLIKLARI:
        raise ValueError("Invalid sector.")
    if len(malzemeler) == 0:
        return []
    agirliklar = SEKTOR_AGIRLIKLARI[sektor]
    ozellikler = [
        "tensile_strength",
        "elastic_modulus",
        "density",
        "max_temp",
        "corrosion_resistance",
        "cost"
    ]
    min_degerler = {}
    max_degerler = {}
    for ozellik in ozellikler:
        en_kucuk = malzemeler[0][ozellik]
        en_buyuk = malzemeler[0][ozellik]
        for eleman in malzemeler:
            deger = eleman[ozellik]
            if deger < en_kucuk:
                en_kucuk = deger
            if deger > en_buyuk:
                en_buyuk = deger
        min_degerler[ozellik] = en_kucuk
        max_degerler[ozellik] = en_buyuk
    sonuc = []
    for eleman in malzemeler:
        toplam = 0.0
        for ozellik in ozellikler:
            en_kucuk = min_degerler[ozellik]
            en_buyuk = max_degerler[ozellik]
            fark = en_buyuk - en_kucuk
            if fark == 0:
                oran = 1.0
            else:
                if ozellik == "density" or ozellik == "cost":
                    oran = (en_buyuk - eleman[ozellik]) / fark
                else:
                    oran = (eleman[ozellik] - en_kucuk) / fark
            agirlikli = oran * agirliklar[ozellik]
            toplam += agirlikli
        yeni_satir = {
            "name": eleman["name"],
            "category": eleman["category"],
            "density": eleman["density"],
            "tensile_strength": eleman["tensile_strength"],
            "elastic_modulus": eleman["elastic_modulus"],
            "specific_strength": round(eleman["tensile_strength"] / eleman["density"], 1),
            "max_temp": eleman["max_temp"],
            "corrosion_resistance": eleman["corrosion_resistance"],
            "cost": eleman["cost"],
            "score": round(toplam * 100, 1)
        }
        sonuc.append(yeni_satir)
    uzunluk = len(sonuc)
    indeks = 0
    while indeks < uzunluk:
        ic_indeks = indeks + 1
        while ic_indeks < uzunluk:
            if sonuc[ic_indeks]["score"] > sonuc[indeks]["score"]:
                gecici = sonuc[indeks]
                sonuc[indeks] = sonuc[ic_indeks]
                sonuc[ic_indeks] = gecici
            ic_indeks += 1
        indeks += 1
    return sonuc
def format_tables(sirali_liste, elenenler):
    metin = "\n=== Recommended Materials (Ranked) ===\n"
    if len(sirali_liste) > 0:
        basliklar = [
            "Rank",
            "Material",
            "Class",
            "Density (g/cm3)",
            "Tensile (MPa)",
            "Modulus (GPa)",
            "Spec. Str.",
            "Max Temp (C)",
            "Corr.",
            "Cost ($/kg)",
            "Score"
        ]
        tablo_satirlari = []
        sayac = 1
        for eleman in sirali_liste:
            satir = [
                sayac,
                eleman["name"],
                eleman["category"],
                eleman["density"],
                eleman["tensile_strength"],
                eleman["elastic_modulus"],
                eleman["specific_strength"],
                eleman["max_temp"],
                eleman["corrosion_resistance"],
                eleman["cost"],
                eleman["score"]
            ]
            tablo_satirlari.append(satir)
            sayac += 1
        metin += tabulate(tablo_satirlari, headers=basliklar, tablefmt="grid")
    else:
        metin += "No materials matched all engineering conditions."
    metin += "\n\n=== Eliminated Materials (Summary) ===\n"
    if len(elenenler) > 0:
        elenen_satirlar = []
        for eleman in elenenler:
            elenen_satirlar.append([
                eleman["name"],
                eleman["category"],
                eleman["reasons"]
            ])
        metin += tabulate(
            elenen_satirlar,
            headers=["Material", "Class", "Elimination Reasons"],
            tablefmt="grid"
        )
    else:
        metin += "No materials were eliminated."
    return metin
def get_sector():
    print("Select Target Sector:")
    print("1. Automotive")
    print("2. Aerospace")
    print("3. Rail")
    secenekler = {
        "1": "automotive",
        "automotive": "automotive",
        "2": "aerospace",
        "aerospace": "aerospace",
        "3": "rail",
        "rail": "rail"
    }
    while True:
        girdi = input("Choice (1-3 or name): ").strip().lower()
        if girdi in secenekler:
            return secenekler[girdi]
        print("Invalid choice. Enter 1, 2, 3 or sector name.")
def get_float_input(mesaj):
    while True:
        girdi = input(mesaj).strip()
        if girdi == "":
            return None
        try:
            deger = float(girdi)
            if deger < 0:
                print("Value cannot be negative.")
            else:
                return deger
        except ValueError:
            print("Please enter a valid number or press Enter to skip.")
def main():
    print("\n=== Engineering Material Selector (MSE) ===")
    malzemeler = load_materials(DB_PATH)
    sektor = get_sector()
    print("\nEnter operating conditions (press Enter to skip any limit):")
    kosullar = {
        "min_tensile": get_float_input("Minimum tensile strength (MPa): "),
        "min_modulus": get_float_input("Minimum elastic modulus (GPa): "),
        "min_temp": get_float_input("Operating temperature (C): "),
        "max_cost": get_float_input("Maximum cost (USD/kg): "),
        "min_corrosion": get_float_input("Minimum corrosion resistance (1-10): ")
    }
    uygunlar, elenenler = filter_materials(malzemeler, kosullar)
    sirali_liste = rank_materials(uygunlar, sektor)
    sonuc = format_tables(sirali_liste, elenenler)
    print(sonuc)
if __name__ == "__main__":
    main()
