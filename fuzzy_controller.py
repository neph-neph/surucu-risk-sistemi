import numpy as np
import skfuzzy as fuzz


class UyelikSet:
    def __init__(self, evren):
        self.evren = evren
        self.kumeler = {}

    def trim(self, ad, sol, orta, sag):
        self.kumeler[ad] = fuzz.trimf(self.evren, [sol, orta, sag])

    def trap(self, ad, sol, sol_tepe, sag_tepe, sag):
        self.kumeler[ad] = fuzz.trapmf(self.evren, [sol, sol_tepe, sag_tepe, sag])

    def uyelik(self, deger, ad):
        return float(fuzz.interp_membership(self.evren, self.kumeler[ad], deger))

    def tum_uyelikler(self, deger):
        return {ad: self.uyelik(deger, ad) for ad in self.kumeler}


_HIZ = UyelikSet(np.arange(0, 201, 1))
_HIZ.trap("yavas", 0, 0, 40, 70)
_HIZ.trim("normal", 50, 90, 120)
_HIZ.trap("hizli", 100, 140, 200, 200)

_SURE = UyelikSet(np.arange(0, 12.1, 0.1))
_SURE.trap("kisa", 0, 0, 1, 3)
_SURE.trim("orta", 2, 4, 6)
_SURE.trap("uzun", 5, 7, 12, 12)

_GOZ = UyelikSet(np.arange(0, 31, 1))
_GOZ.trap("az", 0, 0, 12, 17)
_GOZ.trim("orta", 14, 20, 26)
_GOZ.trap("cok", 22, 27, 30, 30)

_YOL = UyelikSet(np.arange(1, 10.1, 0.1))
_YOL.trap("iyi", 1, 1, 3, 5)
_YOL.trim("orta", 3, 5, 7)
_YOL.trap("kotu", 5, 7, 10, 10)

_YAS = UyelikSet(np.arange(18, 81, 1))
_YAS.trap("genc", 18, 18, 23, 32)
_YAS.trim("orta", 27, 42, 57)
_YAS.trap("yasli", 50, 60, 80, 80)

_SAAT = UyelikSet(np.arange(0, 24, 1))
_SAAT.trap("gunduz", 6, 8, 17, 19)
_SAAT.trim("aksam", 17, 20, 23)
# Gece saatlerini kapsamak icin 0-7 araligi ile 20-23 araligini birlestiriyoruz (dairesel gecis)
_SAAT.kumeler["gece"] = np.maximum(
    fuzz.trapmf(_SAAT.evren, [-1, -1, 5, 7]),
    fuzz.trapmf(_SAAT.evren, [20, 23, 24, 24])
)

_UYKU = UyelikSet(np.arange(0, 12.1, 0.1))
_UYKU.trap("yetersiz", 0, 0, 4, 6)
_UYKU.trim("normal", 5, 7, 9)
_UYKU.trap("iyi", 8, 9, 12, 12)


_GIRDILER = {
    "hiz": _HIZ, "sure": _SURE, "goz": _GOZ, "yol": _YOL,
    "yas": _YAS, "saat": _SAAT, "uyku": _UYKU,
}


_RISK = UyelikSet(np.arange(0, 101, 1))
_RISK.trap("dusuk", 0, 0, 10, 25)
_RISK.trim("orta", 20, 38, 55)
_RISK.trim("yuksek", 50, 65, 80)
_RISK.trap("kritik", 75, 90, 100, 100)

_ONERI = UyelikSet(np.arange(0, 10.1, 0.1))
_ONERI.trap("devam", 0, 0, 1.5, 3)
_ONERI.trim("dikkat", 2, 4, 6)
_ONERI.trim("mola", 5, 6.5, 8)
_ONERI.trap("durdur", 7.5, 9, 10, 10)

_CIKTILAR = {"risk": _RISK, "oneri": _ONERI}


_RISK_TEMSIL = {"dusuk": 10.0, "orta": 38.0, "yuksek": 65.0, "kritik": 92.0}
_ONERI_TEMSIL = {"devam": 1.0, "dikkat": 4.0, "mola": 6.5, "durdur": 9.2}


_KURALLAR = [
    ({"hiz": "yavas", "sure": "kisa", "goz": "az", "yol": "iyi"}, "dusuk", "devam"),
    ({"hiz": "normal", "sure": "kisa", "goz": "az", "yol": "iyi", "uyku": "iyi"}, "dusuk", "devam"),
    ({"hiz": "yavas", "sure": "orta", "goz": "az", "yol": "iyi"}, "dusuk", "devam"),
    ({"hiz": "normal", "sure": "kisa", "goz": "az", "yol": "iyi", "saat": "gunduz"}, "dusuk", "devam"),
    ({"hiz": "yavas", "sure": "kisa", "goz": "az", "uyku": "iyi"}, "dusuk", "devam"),
    ({"hiz": "yavas", "sure": "kisa", "goz": "az", "yas": "orta"}, "dusuk", "devam"),
    ({"hiz": "normal", "sure": "kisa", "goz": "az", "uyku": "normal", "saat": "gunduz"}, "dusuk", "devam"),
    ({"hiz": "yavas", "sure": "kisa", "uyku": "iyi", "saat": "gunduz"}, "dusuk", "devam"),
    ({"hiz": "normal", "sure": "orta", "goz": "az", "yol": "iyi"}, "orta", "dikkat"),
    ({"hiz": "hizli", "sure": "kisa", "goz": "az", "yol": "iyi"}, "orta", "dikkat"),
    ({"hiz": "normal", "sure": "kisa", "goz": "orta", "yol": "iyi"}, "orta", "dikkat"),
    ({"hiz": "yavas", "sure": "uzun", "goz": "az", "yol": "iyi"}, "orta", "dikkat"),
    ({"hiz": "yavas", "sure": "kisa", "goz": "az", "yol": "kotu"}, "orta", "dikkat"),
    ({"hiz": "normal", "sure": "kisa", "goz": "az", "yas": "genc"}, "orta", "dikkat"),
    ({"hiz": "normal", "sure": "kisa", "goz": "az", "yas": "yasli"}, "orta", "dikkat"),
    ({"hiz": "normal", "sure": "orta", "goz": "orta", "yol": "iyi"}, "orta", "dikkat"),
    ({"hiz": "yavas", "sure": "orta", "goz": "orta", "yol": "orta"}, "orta", "dikkat"),
    ({"hiz": "normal", "sure": "orta", "goz": "az", "yol": "orta"}, "orta", "dikkat"),
    ({"saat": "aksam", "goz": "az", "hiz": "normal"}, "orta", "dikkat"),
    ({"uyku": "normal", "sure": "kisa", "goz": "az"}, "orta", "dikkat"),
    ({"hiz": "normal", "goz": "orta", "uyku": "normal"}, "orta", "dikkat"),
    ({"hiz": "hizli", "sure": "orta", "goz": "orta", "yol": "iyi"}, "yuksek", "mola"),
    ({"hiz": "normal", "sure": "uzun", "goz": "orta", "yol": "iyi"}, "yuksek", "mola"),
    ({"hiz": "normal", "sure": "orta", "goz": "cok", "yol": "iyi"}, "yuksek", "mola"),
    ({"hiz": "hizli", "sure": "kisa", "goz": "az", "yol": "kotu"}, "yuksek", "mola"),
    ({"hiz": "normal", "sure": "orta", "goz": "orta", "yol": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "sure": "orta", "goz": "az", "yol": "orta"}, "yuksek", "mola"),
    ({"sure": "uzun", "goz": "cok"}, "yuksek", "mola"),
    ({"goz": "cok", "yol": "kotu"}, "yuksek", "mola"),
    ({"yol": "kotu", "hiz": "hizli"}, "yuksek", "mola"),
    ({"hiz": "hizli", "yas": "yasli"}, "yuksek", "mola"),
    ({"saat": "gece", "sure": "uzun"}, "yuksek", "mola"),
    ({"uyku": "yetersiz", "sure": "orta"}, "yuksek", "mola"),
    ({"uyku": "yetersiz", "goz": "orta"}, "yuksek", "mola"),
    ({"saat": "aksam", "uyku": "yetersiz"}, "yuksek", "mola"),
    ({"saat": "gece", "goz": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "sure": "uzun", "goz": "cok"}, "kritik", "durdur"),
    ({"sure": "uzun", "goz": "cok", "yol": "kotu"}, "kritik", "durdur"),
    ({"hiz": "hizli", "goz": "cok", "yol": "kotu"}, "kritik", "durdur"),
    ({"hiz": "hizli", "sure": "uzun", "yol": "kotu"}, "kritik", "durdur"),
    ({"hiz": "normal", "sure": "uzun", "goz": "cok", "yol": "kotu"}, "kritik", "durdur"),
    ({"hiz": "hizli", "sure": "uzun", "yas": "yasli"}, "kritik", "durdur"),
    ({"hiz": "hizli", "goz": "cok", "yas": "genc"}, "kritik", "durdur"),
    ({"sure": "uzun", "goz": "cok", "yas": "yasli"}, "kritik", "durdur"),
    ({"hiz": "hizli", "goz": "cok", "yol": "orta"}, "kritik", "durdur"),
    ({"saat": "gece", "uyku": "yetersiz", "sure": "orta"}, "kritik", "durdur"),
    ({"saat": "gece", "goz": "cok"}, "kritik", "durdur"),
    ({"uyku": "yetersiz", "goz": "cok"}, "kritik", "durdur"),
    ({"uyku": "yetersiz", "hiz": "hizli", "saat": "gece"}, "kritik", "durdur"),
    ({"saat": "gece", "sure": "uzun", "uyku": "yetersiz"}, "kritik", "durdur"),
    ({"hiz": "hizli", "goz": "cok", "uyku": "yetersiz"}, "kritik", "durdur"),
    ({"yol": "kotu", "uyku": "yetersiz", "saat": "gece"}, "kritik", "durdur"),
    ({"sure": "uzun", "uyku": "yetersiz", "yas": "yasli"}, "kritik", "durdur"),
    ({"hiz": "hizli", "uyku": "yetersiz", "saat": "aksam"}, "kritik", "durdur"),
    ({"sure": "uzun", "goz": "cok", "uyku": "yetersiz"}, "kritik", "durdur"),
    ({"hiz": "hizli", "goz": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "sure": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "yol": "orta"}, "yuksek", "mola"),
    ({"goz": "orta", "yol": "orta"}, "orta", "dikkat"),
    ({"sure": "uzun", "yol": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "uyku": "normal", "sure": "orta"}, "yuksek", "mola"),
    ({"hiz": "normal", "goz": "orta", "yol": "orta"}, "yuksek", "mola"),
    ({"hiz": "hizli", "goz": "cok"}, "kritik", "durdur"),
    ({"hiz": "hizli", "sure": "uzun"}, "kritik", "durdur"),
    ({"sure": "uzun", "yol": "kotu"}, "kritik", "durdur"),
]


GIRDI_BILGI = {
    "hiz": {"baslik": "Arac hizi", "birim": "km/h", "min": 0, "max": 200, "varsayilan": 90, "adim": 5},
    "sure": {"baslik": "Surus suresi", "birim": "saat", "min": 0.0, "max": 12.0, "varsayilan": 3.0, "adim": 0.5},
    "goz": {"baslik": "Goz kapanma sayisi", "birim": "kez/dakika", "min": 0, "max": 30, "varsayilan": 17, "adim": 1},
    "yol": {"baslik": "Yol durumu", "birim": "1=iyi  10=kotu", "min": 1.0, "max": 10.0, "varsayilan": 4.0, "adim": 0.5},
    "yas": {"baslik": "Surucu yasi", "birim": "yil", "min": 18, "max": 80, "varsayilan": 35, "adim": 1},
    "saat": {"baslik": "Gunun saati", "birim": "0-23", "min": 0, "max": 23, "varsayilan": 14, "adim": 1},
    "uyku": {"baslik": "Son 24 saatte uyku", "birim": "saat", "min": 0.0, "max": 12.0, "varsayilan": 7.0, "adim": 0.5},
}


SONUC_RENGI = {
    "DUSUK": "#16a34a", "ORTA": "#ca8a04", "YUKSEK": "#ea580c", "KRITIK": "#b91c1c",
    "DEVAM ET": "#16a34a", "DIKKAT": "#ca8a04", "MOLA VER": "#ea580c", "DURDUR": "#b91c1c",
}


def _clip(degerler):
    out = {}
    for ad, bilgi in GIRDI_BILGI.items():
        out[ad] = float(np.clip(degerler[ad], bilgi["min"], bilgi["max"]))
    return out


def _uyelikleri_hesapla(deger):
    return {ad: _GIRDILER[ad].tum_uyelikler(deger[ad]) for ad in _GIRDILER}


def _kural_kuvveti(sartlar, uyelik):
    return min(uyelik[g][k] for g, k in sartlar.items())


def _aktif_kurallari_bul(uyelik):
    aktif = []
    for i, (sartlar, risk_k, oneri_k) in enumerate(_KURALLAR, start=1):
        kuv = _kural_kuvveti(sartlar, uyelik)
        if kuv > 0.001:
            aktif.append({
                "no": i,
                "sartlar": sartlar,
                "risk_kumesi": risk_k,
                "oneri_kumesi": oneri_k,
                "kuvvet": kuv,
                "metin": " AND ".join(f"{g}={k}" for g, k in sartlar.items()),
                "sonuc_etiketi": risk_k.upper() + " / " + {"devam": "DEVAM ET", "dikkat": "DIKKAT", "mola": "MOLA VER", "durdur": "DURDUR"}[oneri_k],
            })
    aktif.sort(key=lambda x: x["kuvvet"], reverse=True)
    return aktif


def _agrege_egri(aktif, cikti_set, anahtar):
    evren = cikti_set.evren
    sonuc = np.zeros_like(evren, dtype=float)
    for k in aktif:
        kume = cikti_set.kumeler[k[anahtar]]
        sonuc = np.maximum(sonuc, np.minimum(k["kuvvet"], kume))
    return sonuc


def _hiyerarsik_centroid(aktif, temsil, sira):
    kategori_max = {kat: 0.0 for kat in sira}
    for k in aktif:
        kat = k["risk_kumesi"]
        if k["kuvvet"] > kategori_max[kat]:
            kategori_max[kat] = k["kuvvet"]
    risk = 0.0
    kalan = 1.0
    for kat in sira:
        kuv = kategori_max[kat]
        risk += kuv * temsil[kat] * kalan
        kalan *= (1.0 - kuv)
    return risk


def _hiyerarsik_centroid_oneri(aktif, temsil, sira):
    kategori_max = {kat: 0.0 for kat in sira}
    for k in aktif:
        kat = k["oneri_kumesi"]
        if k["kuvvet"] > kategori_max[kat]:
            kategori_max[kat] = k["kuvvet"]
    sonuc = 0.0
    kalan = 1.0
    for kat in sira:
        kuv = kategori_max[kat]
        sonuc += kuv * temsil[kat] * kalan
        kalan *= (1.0 - kuv)
    return sonuc


def _egri_centroid(evren, agregat):
    toplam = agregat.sum()
    if toplam <= 1e-9:
        return 0.0
    return float((evren * agregat).sum() / toplam)


def risk_hesapla(hiz=90, sure=3.0, goz=17, yol=4.0, yas=35, saat=14, uyku=7.0):
    g = _clip({"hiz": hiz, "sure": sure, "goz": goz, "yol": yol,
               "yas": yas, "saat": saat, "uyku": uyku})
    uyelik = _uyelikleri_hesapla(g)
    aktif = _aktif_kurallari_bul(uyelik)

    if not aktif:
        return {
            "risk": 0.0, "kategori": "DUSUK",
            "kategori_uyelikleri": {"DUSUK": 1.0, "ORTA": 0.0, "YUKSEK": 0.0, "KRITIK": 0.0},
            "oneri_skor": 0.0, "oneri_metin": "DEVAM ET",
            "oneri_uyelikleri": {"DEVAM ET": 1.0, "DIKKAT": 0.0, "MOLA VER": 0.0, "DURDUR": 0.0},
            "uyelik_girisleri": uyelik, "aktif_kurallar": [], "girdi_clipped": g,
            "risk_agregat": np.zeros_like(_RISK.evren), "oneri_agregat": np.zeros_like(_ONERI.evren),
        }

    risk_d = _hiyerarsik_centroid(aktif, _RISK_TEMSIL, ["kritik", "yuksek", "orta", "dusuk"])
    oneri_d = _hiyerarsik_centroid_oneri(aktif, _ONERI_TEMSIL, ["durdur", "mola", "dikkat", "devam"])
    risk_agr = _agrege_egri(aktif, _RISK, "risk_kumesi")
    oneri_agr = _agrege_egri(aktif, _ONERI, "oneri_kumesi")

    kat_uye = {
        "DUSUK": _RISK.uyelik(risk_d, "dusuk"),
        "ORTA": _RISK.uyelik(risk_d, "orta"),
        "YUKSEK": _RISK.uyelik(risk_d, "yuksek"),
        "KRITIK": _RISK.uyelik(risk_d, "kritik"),
    }
    kategori = max(kat_uye, key=kat_uye.get)

    oneri_uye = {
        "DEVAM ET": _ONERI.uyelik(oneri_d, "devam"),
        "DIKKAT": _ONERI.uyelik(oneri_d, "dikkat"),
        "MOLA VER": _ONERI.uyelik(oneri_d, "mola"),
        "DURDUR": _ONERI.uyelik(oneri_d, "durdur"),
    }
    oneri_metin = max(oneri_uye, key=oneri_uye.get)

    return {
        "risk": risk_d, "kategori": kategori, "kategori_uyelikleri": kat_uye,
        "oneri_skor": oneri_d, "oneri_metin": oneri_metin, "oneri_uyelikleri": oneri_uye,
        "uyelik_girisleri": uyelik, "aktif_kurallar": aktif, "girdi_clipped": g,
        "risk_agregat": risk_agr, "oneri_agregat": oneri_agr,
    }


def klasik_risk_hesapla(hiz=90, sure=3.0, goz=17, yol=4.0, yas=35, saat=14, uyku=7.0):
    p = 0
    if hiz > 130: p += 28
    elif hiz > 90: p += 16
    elif hiz > 60: p += 6
    if sure > 7: p += 22
    elif sure > 4: p += 12
    elif sure > 2: p += 5
    if goz > 23: p += 22
    elif goz > 17: p += 12
    if yol > 7: p += 16
    elif yol > 4: p += 8
    if yas < 25 or yas > 65: p += 8
    if saat <= 5 or saat >= 22: p += 10
    if uyku < 5: p += 18
    elif uyku < 7: p += 6
    p = min(p, 100)
    if p < 25: k = "DUSUK"
    elif p < 55: k = "ORTA"
    elif p < 80: k = "YUKSEK"
    else: k = "KRITIK"
    return {"risk": p, "kategori": k}


def risk_farkli_yontemlerle(hiz=90, sure=3.0, goz=17, yol=4.0, yas=35, saat=14, uyku=7.0):
    s = risk_hesapla(hiz, sure, goz, yol, yas, saat, uyku)
    agr = s["risk_agregat"]
    if agr.sum() <= 1e-9:
        return {"weighted_centroid": s["risk"], "egri_centroid": 0.0, "bisector": 0.0, "mom": 0.0}
    return {
        "weighted_centroid": s["risk"],
        "egri_centroid": _egri_centroid(_RISK.evren, agr),
        "bisector": float(fuzz.defuzz(_RISK.evren, agr, "bisector")),
        "mom": float(fuzz.defuzz(_RISK.evren, agr, "mom")),
    }


GIRDILER = _GIRDILER
CIKTILAR = _CIKTILAR
KURAL_SAYISI = len(_KURALLAR)
RISK_TEMSIL = _RISK_TEMSIL
ONERI_TEMSIL = _ONERI_TEMSIL
