# Surucu Yorgunlugu ve Kaza Risk Degerlendirme Sistemi

**Bulanik Mantik Donem Projesi**
Ali Alizada - 21703903

Surucunun anlik durumuna gore (hiz, surus suresi, goz kapanma sayisi, yol durumu, yas, gunun saati, son uyku suresi) bulanik mantikla kaza riski yuzdesi ve sistem onerisi hesaplayan bir karar destek sistemi. Gelismis Surucu Yardim Sistemleri (ADAS) icin bir prototip uygulamadir.

## Tek Bakista Proje

| Ozellik | Deger |
|---|---|
| Girdi sayisi | 7 |
| Cikti sayisi | 2 (Risk + Oneri) |
| Bulanik kural sayisi | 65 |
| Her girdi icin dilsel etiket | 3 |
| Cikti kategorileri | 4 (Dusuk / Orta / Yuksek / Kritik) |
| Cikarim motoru | Mamdani min-max |
| Durulastirma | Hiyerarsik weighted centroid (5 yontem karsilastirmali) |
| Arayuz | Streamlit (7 sekme, interaktif slider) |
| Klasik karsilastirma | Esik tabanli sistemle yan yana |

## Kurulum ve Calistirma

```bash
pip install -r requirements.txt
py -m streamlit run app.py
```

Komut satirindan toplu test:
```bash
py test_senaryolari.py
```

## Sistem Tasarimi

### Girdiler

| Girdi | Aralik | Dilsel Etiketler | Aciklama |
|---|---|---|---|
| Arac hizi | 0-200 km/h | Yavas / Normal / Hizli | Anlik arac hizi |
| Surus suresi | 0-12 saat | Kisa / Orta / Uzun | Aralisiz direksiyon basinda gecen sure |
| Goz kapanma sayisi | 0-30 kez/dk | Az / Orta / Cok | PERCLOS metrigi yaklasiklamasi |
| Yol durumu | 1-10 | Iyi / Orta / Kotu | 1=kuru-temiz, 10=karli-buzlu |
| Surucu yasi | 18-80 yil | Genc / Orta / Yasli | Refleks ve deneyim ile korele |
| Gunun saati | 0-23 | Gunduz / Aksam / Gece | Circadian rhythm (gece 3x daha riskli) |
| Son 24 saat uyku | 0-12 saat | Yetersiz / Normal / Iyi | Sleep deprivation (NHTSA standardi) |

### Ciktilar

| Cikti | Aralik | Kategoriler |
|---|---|---|
| Kaza riski | 0-100% | Dusuk / Orta / Yuksek / Kritik |
| Sistem onerisi | 0-10 skor | DEVAM ET / DIKKAT / MOLA VER / DURDUR |

### Uyelik Fonksiyonlari

Her degisken icin 3 dilsel etiket tanimlandi. Ucgen (trimf) ve yamuk (trapmf) uyelik fonksiyonlari kullanildi. Ucgen orta etiketlerde tek tepe verir, yamuk uc etiketlerde genis "tam uyelik" araligi saglar.

![Girdi uyelik fonksiyonlari](gorsel/01_uyelik_fonksiyonlari.png)

![Cikti uyelik fonksiyonlari](gorsel/02_cikis_uyelikleri.png)

## Bulgular ve Kanitlar

### 1. Monotonluk Kaniti

Sistem her risk faktoru artirildiginda riskin artmasini (ya da en azindan azalmamasini) garanti eder.

![Monotonluk kaniti](gorsel/03_monotonluk_kaniti.png)

- Hiz artarken risk monoton artiyor (KRITIK durumda zaten tepede)
- Goz kapanma artarken risk artiyor (32 → 64)
- Uyku azaldikca risk artiyor (34 → 50)
- Saat 22'den sonra ve sabah 6'ya kadar belirgin risk sicramasi (gece riski)

### 2. 7 Senaryoda Klasik vs Bulanik Karsilastirma

![Senaryo karsilastirma](gorsel/04_senaryo_karsilastirma.png)

| Senaryo | Bulanik | Klasik | Aciklama |
|---|---:|---:|---|
| Sehir ici sakin | ~12% | ~0% | Klasik "tamamen risksiz" der, bulanik dogal taban riski tutar |
| Otoyol dinlenmis | ~29% | ~16% | Bulanik gece olmasa bile orta dikkat oneriyor |
| Genc hizli surucu | ~52% | ~32% | Genc surucu yas riskini bulanik daha iyi yakaliyor |
| Uzun yolculuk yorgun | ~62% | ~50% | Yorgunluk + sure + zaman birlesimi guclu |
| Yasli surucu kotu yol | ~78% | ~50% | Bulanik yas + yol kombinasyonunu vurgular |
| Gece - uyku eksik | ~70% | ~58% | Uyku + saat + goz kombinasyonu |
| TEHLIKELI kombinasyon | ~93% | 100% | Bulanik abartmiyor, klasik anlamsiz sekilde tavana yapisiyor |

### 3. Aktif Kurallarin Tetiklenmesi

TEHLIKELI senaryoda en guclu 12 kural ve katkilari:

![Aktif kurallar](gorsel/05_aktif_kurallar.png)

### 4. Durulastirma Yontemleri Karsilastirmasi

4 farkli durulastirma yontemiyle ayni senaryoda risk hesaplandi:

![Durulastirma karsilastirma](gorsel/06_durulastirma_karsilastirma.png)

Yontemler arasi tutarlilik sistem dogrulugunun isareti. Mean of Maxima yuksek senaryoda biraz daha keskin sonuc verirken, weighted centroid en dengeli ve monoton sonuc uretir.

### 5. Hiyerarsik Agregasyon - Bug Cozumu

Klasik weighted average centroid'in problemi: KRITIK kural aktifken, daha dusuk kategoriden yeni kural eklenince ortalama asagi cekilir (monotonluk bozulur). Bu sistemde **hiyerarsik agregasyon** kullanildi: kategoriler oncelik sirasiyla degerlendirilir, ust kategori once payini alir.

![Hiyerarsik agregasyon aciklamasi](gorsel/07_hiyerarsik_aciklama.png)

## Teknik Ozellikler

- **Hiyerarsik weighted centroid durulastirma**: standart agirlikli ortalamada olusan monotonluk ihlalini matematiksel olarak coker
- **4 farkli durulastirma yontemi karsilastirmasi**: Weighted Centroid, Egri Centroid, Bisector, Mean of Maxima
- **Klasik esik tabanli sistemle yan yana karsilastirma**: bulanik mantigin yumusak gecis avantajinin somut gosterimi
- **Aciklanabilirlik paneli**: her sonuc icin tetiklenen kurallar ve girdi uyelikleri detayli gosterilir
- **7 hazir senaryo**: hizli demo ve sistematik test icin
- **CSV indirme**: sonuclarin diger araclara aktarimi
- **Cift cikti yapisi**: sayisal risk yuzdesi + somut karar onerisi (DEVAM ET / DIKKAT / MOLA VER / DURDUR)
- **Bilimsel temel**: PERCLOS (Wierwille 1994), NHTSA ve WHO standartlarina dayali esik degerleri

## Dosyalar

```
fuzzy_controller.py        Bulanik mantik cekirdegi (65 kural)
app.py                     Streamlit interaktif arayuz
test_senaryolari.py        10 senaryolu otomatik test
requirements.txt           Python paketleri
README.md                  Bu dosya
RAPOR.docx                 Detayli proje raporu
gorsel/                    Bulguların grafikleri (7 PNG)
```

## Kaynakca

- Zadeh, L. A. (1965). Fuzzy sets. *Information and Control*, 8(3), 338-353.
- Mamdani, E. H. (1974). Application of fuzzy algorithms for control. *Proceedings of the IEE*, 121(12).
- Wierwille, W. W., & Ellsworth, L. A. (1994). Evaluation of driver drowsiness by trained raters. *Accident Analysis & Prevention*, 26(5), 571-581. (PERCLOS)
- NHTSA (2017). Drowsy Driving Research and Program Plan.
- WHO (2023). Global Status Report on Road Safety.
- scikit-fuzzy documentation: https://pythonhosted.org/scikit-fuzzy/
