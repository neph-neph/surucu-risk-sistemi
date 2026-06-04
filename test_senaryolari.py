"""
Test senaryolari - rapor icin sonuc tablosu uretir.
Calistir: py test_senaryolari.py
"""

import pandas as pd
from fuzzy_controller import risk_hesapla


SENARYOLAR = [
    # (ad, hiz, sure, goz, yol)
    ("Sehir ici - sakin",           50, 1, 10, 2),
    ("Otoyol - dinlenmis surucu",  110, 2, 14, 2),
    ("Trafikte sikis - sabirsiz",   30, 2, 20, 4),
    ("Uzun yolculuk - yorgun",    100, 7, 24, 4),
    ("Gece islak yol - dikkatli",   90, 5, 22, 7),
    ("Tehlikeli kombinasyon",      160, 9, 28, 9),
    ("Sisli hava - yavas",          40, 1, 12, 8),
    ("Yorgun ama yavas",            60, 8, 26, 3),
    ("Aceleci surucu - kuru yol",  170, 2, 13, 2),
    ("Cok uzun aralisiz surus",     85, 11, 25, 3),
]


def main():
    satirlar = []
    for ad, h, s, g, y in SENARYOLAR:
        r = risk_hesapla(h, s, g, y)
        satirlar.append({
            "Senaryo": ad,
            "Hiz (km/h)": h,
            "Sure (saat)": s,
            "Goz (kez/dk)": g,
            "Yol (1-10)": y,
            "Risk (%)": round(r["risk"], 1),
            "Kategori": r["kategori"],
            "Tetiklenen kural": len(r["aktif_kurallar"]),
        })

    df = pd.DataFrame(satirlar)
    print(df.to_string(index=False))
    df.to_csv("test_sonuclari.csv", index=False, encoding="utf-8-sig")
    print("\n--> test_sonuclari.csv kaydedildi.")


if __name__ == "__main__":
    main()
