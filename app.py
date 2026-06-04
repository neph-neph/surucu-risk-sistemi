import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from fuzzy_controller import (
    GIRDILER, CIKTILAR, GIRDI_BILGI, SONUC_RENGI, KURAL_SAYISI,
    RISK_TEMSIL, ONERI_TEMSIL,
    risk_hesapla, klasik_risk_hesapla, risk_farkli_yontemlerle,
)


st.set_page_config(
    page_title="Surucu Risk Sistemi",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }
    h1 { font-size: 1.7rem !important; margin-bottom: 0 !important; padding-bottom: 0 !important; }
    .stMetric { background: rgba(120, 120, 120, 0.05); padding: 14px 18px; border-radius: 8px; border-left: 4px solid #888; }
    .result-card {
        padding: 18px 22px;
        border-radius: 8px;
        border-left: 5px solid var(--c);
        background: rgba(120, 120, 120, 0.08);
    }
    .result-card .label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.75; }
    .result-card .value { font-size: 36px; font-weight: 700; line-height: 1.1; color: var(--c); margin-top: 4px; }
    .rule-row {
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 6px;
        border-left: 3px solid var(--c);
        background: rgba(120, 120, 120, 0.08);
        font-size: 13px;
    }
    .rule-row code { font-size: 12px; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; font-size: 13px; }
    section[data-testid="stSidebar"] { background: rgba(120, 120, 120, 0.03); }
</style>
""", unsafe_allow_html=True)


st.markdown("### Surucu Yorgunlugu ve Kaza Risk Degerlendirme Sistemi")
st.caption(f"Bulanik Mantik Donem Projesi  |  7 girdi  •  2 cikti  •  {KURAL_SAYISI} kural  •  Centroid durulastirma")


HAZIR = {
    "Manuel": None,
    "Sehir ici - sakin gunduz": {"hiz": 50, "sure": 1.0, "goz": 10, "yol": 2.0, "yas": 35, "saat": 14, "uyku": 8.0},
    "Otoyol - dinlenmis surucu": {"hiz": 110, "sure": 2.0, "goz": 14, "yol": 2.0, "yas": 35, "saat": 11, "uyku": 8.0},
    "Genc hizli surucu": {"hiz": 140, "sure": 1.5, "goz": 13, "yol": 3.0, "yas": 22, "saat": 16, "uyku": 7.0},
    "Uzun yolculuk yorgun": {"hiz": 100, "sure": 7.0, "goz": 24, "yol": 4.0, "yas": 45, "saat": 17, "uyku": 6.0},
    "Yasli surucu kotu yol": {"hiz": 90, "sure": 5.0, "goz": 18, "yol": 7.0, "yas": 68, "saat": 19, "uyku": 7.0},
    "Gece surusu - uyku eksik": {"hiz": 100, "sure": 4.0, "goz": 22, "yol": 5.0, "yas": 35, "saat": 2, "uyku": 4.0},
    "TEHLIKELI kombinasyon": {"hiz": 160, "sure": 9.0, "goz": 28, "yol": 9.0, "yas": 70, "saat": 3, "uyku": 3.0},
}


with st.sidebar:
    st.markdown("**Senaryolar**")
    hazir_sec = st.selectbox("Hazir senaryo", list(HAZIR.keys()), label_visibility="collapsed")
    secilen = HAZIR.get(hazir_sec)

    st.markdown("---")
    st.markdown("**Giris Degerleri**")
    degerler = {}
    for ad, bilgi in GIRDI_BILGI.items():
        d = secilen[ad] if secilen else bilgi["varsayilan"]
        degerler[ad] = st.slider(
            f"{bilgi['baslik']}  ({bilgi['birim']})",
            float(bilgi["min"]), float(bilgi["max"]), float(d), float(bilgi["adim"]),
            key=f"sl_{ad}_{hazir_sec}",
        )

    st.markdown("---")
    hesapla_btn = st.button("HESAPLA", type="primary", use_container_width=True)
    otomatik = st.checkbox("Otomatik hesapla", value=True)


if hesapla_btn or otomatik:
    s = risk_hesapla(**degerler)
    risk_v = s["risk"]
    kategori = s["kategori"]
    oneri_m = s["oneri_metin"]
    aktif = s["aktif_kurallar"]

    rk = SONUC_RENGI[kategori]
    ro = SONUC_RENGI[oneri_m]

    c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.4, 1])
    with c1:
        st.markdown(f"<div class='result-card' style='--c:{rk}'><div class='label'>Kaza Riski</div><div class='value'>{risk_v:.1f}%</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='result-card' style='--c:{rk}'><div class='label'>Risk Kategorisi</div><div class='value' style='font-size:26px'>{kategori}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='result-card' style='--c:{ro}'><div class='label'>Sistem Onerisi</div><div class='value' style='font-size:24px'>{oneri_m}</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='result-card' style='--c:#3b82f6'><div class='label'>Aktif Kural</div><div class='value'>{len(aktif)}/{KURAL_SAYISI}</div></div>", unsafe_allow_html=True)

    st.markdown("")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Genel Sonuc", "Uyelik Fonksiyonlari", "Aktif Kurallar",
        "Aciklanabilirlik", "Durulastirma", "Klasik vs Bulanik", "Test Senaryolari",
    ])

    with tab1:
        col_a, col_b = st.columns([1.2, 1])
        with col_a:
            fig, ax = plt.subplots(figsize=(7, 1.6), constrained_layout=True)
            for i, (et, rng, cl) in enumerate([
                ("DUSUK", (0, 25), "#16a34a"),
                ("ORTA", (25, 50), "#ca8a04"),
                ("YUKSEK", (50, 75), "#ea580c"),
                ("KRITIK", (75, 100), "#b91c1c"),
            ]):
                ax.barh(0, rng[1] - rng[0], left=rng[0], height=0.4, color=cl, alpha=0.85, edgecolor="white", linewidth=2)
                ax.text((rng[0] + rng[1]) / 2, -0.5, et, ha="center", fontsize=9, color=cl, weight="bold")
            ax.plot([risk_v, risk_v], [-0.25, 0.25], color="black", linewidth=3)
            ax.scatter([risk_v], [0], s=120, color="black", zorder=5)
            ax.text(risk_v, 0.45, f"{risk_v:.1f}%", ha="center", fontsize=12, weight="bold")
            ax.set_xlim(0, 100); ax.set_ylim(-0.8, 0.7)
            ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
            ax.spines[["top", "left", "right"]].set_visible(False)
            ax.set_xlabel("Risk %", fontsize=9)
            st.pyplot(fig); plt.close(fig)

            fig, ax = plt.subplots(figsize=(7, 2.2), constrained_layout=True)
            cats = ["DUSUK", "ORTA", "YUKSEK", "KRITIK"]
            vals = [s["kategori_uyelikleri"][c] for c in cats]
            cols = ["#16a34a", "#ca8a04", "#ea580c", "#b91c1c"]
            bars = ax.barh(cats, vals, color=cols)
            for b, v in zip(bars, vals):
                ax.text(v + 0.02, b.get_y() + b.get_height() / 2, f"{v:.2f}", va="center", fontsize=10, weight="bold")
            ax.set_xlim(0, 1.1); ax.set_xlabel("Cikis kume uyelikleri")
            ax.spines[["top", "right"]].set_visible(False)
            st.pyplot(fig); plt.close(fig)

        with col_b:
            st.markdown("**Sistem Onerisi - Bulanik Dagilim**")
            for ad, val in s["oneri_uyelikleri"].items():
                r = SONUC_RENGI[ad]
                st.markdown(
                    f"<div style='margin-bottom:6px'><div style='display:flex; justify-content:space-between; font-size:13px'>"
                    f"<span style='color:{r}; font-weight:600'>{ad}</span><span>{val:.2f}</span></div>"
                    f"<div style='background:#80808033; height:8px; border-radius:4px; overflow:hidden'>"
                    f"<div style='width:{val * 100:.0f}%; height:100%; background:{r}'></div></div></div>",
                    unsafe_allow_html=True,
                )

    with tab2:
        st.caption("Mavi kesik cizgi giris degerinin yerini gosterir.")
        adlar = list(GIRDILER.keys())
        rows = (len(adlar) + 1) // 2
        fig, axes = plt.subplots(rows, 2, figsize=(13, 2.5 * rows), constrained_layout=True)
        ax_list = axes.flatten()
        for i, ad in enumerate(adlar):
            ax = ax_list[i]
            us = GIRDILER[ad]
            for kume_ad, mf in us.kumeler.items():
                ax.plot(us.evren, mf, linewidth=2, label=kume_ad)
                ax.fill_between(us.evren, mf, alpha=0.12)
            ax.axvline(degerler[ad], color="#1e40af", linestyle="--", linewidth=2, label=f"giris={degerler[ad]}")
            ax.set_title(f"{GIRDI_BILGI[ad]['baslik']}", fontsize=11)
            ax.set_ylim(-0.05, 1.1)
            ax.legend(fontsize=8, loc="upper right")
            ax.grid(alpha=0.2)
        for j in range(len(adlar), len(ax_list)):
            ax_list[j].axis("off")
        st.pyplot(fig); plt.close(fig)

        st.markdown("**Cikis Uyelik Fonksiyonlari**")
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(7, 3), constrained_layout=True)
            us = CIKTILAR["risk"]
            for kume_ad, mf in us.kumeler.items():
                ax.plot(us.evren, mf, linewidth=2, label=kume_ad)
                ax.fill_between(us.evren, mf, alpha=0.12)
            ax.axvline(risk_v, color="#dc2626", linestyle="--", linewidth=2.5, label=f"sonuc={risk_v:.1f}")
            ax.set_title("Risk (cikti)", fontsize=11); ax.set_ylim(-0.05, 1.1)
            ax.legend(fontsize=9); ax.grid(alpha=0.2)
            st.pyplot(fig); plt.close(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(7, 3), constrained_layout=True)
            us = CIKTILAR["oneri"]
            for kume_ad, mf in us.kumeler.items():
                ax.plot(us.evren, mf, linewidth=2, label=kume_ad)
                ax.fill_between(us.evren, mf, alpha=0.12)
            ax.axvline(s["oneri_skor"], color="#dc2626", linestyle="--", linewidth=2.5, label=f"sonuc={s['oneri_skor']:.2f}")
            ax.set_title("Oneri (cikti)", fontsize=11); ax.set_ylim(-0.05, 1.1)
            ax.legend(fontsize=9); ax.grid(alpha=0.2)
            st.pyplot(fig); plt.close(fig)

    with tab3:
        if not aktif:
            st.warning("Hicbir kural tetiklenmedi.")
        else:
            st.caption(f"{len(aktif)} kural tetiklendi. Kuvvet sirali listeleniyor.")
            for k in aktif:
                kat = k["sonuc_etiketi"].split("/")[0].strip()
                cl = SONUC_RENGI.get(kat, "#888")
                st.markdown(
                    f"<div class='rule-row' style='--c:{cl}'>"
                    f"<b>Kural #{k['no']}</b> &nbsp; <span style='color:{cl}'>{k['sonuc_etiketi']}</span> "
                    f"&nbsp;|&nbsp; kuvvet: <b>{k['kuvvet']:.3f}</b><br>"
                    f"<code>IF {k['metin']}</code></div>",
                    unsafe_allow_html=True,
                )

    with tab4:
        st.markdown("**Her girdinin hangi bulanik kumeye ne kadar ait?**")
        cols = st.columns(len(GIRDILER))
        u = s["uyelik_girisleri"]
        for col, ad in zip(cols, GIRDILER.keys()):
            with col:
                st.caption(f"**{GIRDI_BILGI[ad]['baslik']}** ({degerler[ad]})")
                for kume_ad, v in u[ad].items():
                    if v > 0.001:
                        st.markdown(
                            f"<div style='font-size:12px; margin-bottom:4px'>{kume_ad}: <b>{v:.2f}</b>"
                            f"<div style='background:#80808033; height:6px; border-radius:3px; margin-top:2px'>"
                            f"<div style='width:{v * 100:.0f}%; height:100%; background:#3b82f6; border-radius:3px'></div></div></div>",
                            unsafe_allow_html=True,
                        )
        st.markdown("---")
        st.markdown("**Bu sonuc niye cikti?  (en guclu 5 kural)**")
        for k in aktif[:5]:
            kat = k["sonuc_etiketi"].split("/")[0].strip()
            cl = SONUC_RENGI.get(kat, "#888")
            st.markdown(f"<div style='font-size:13px; padding:4px 0'>"
                       f"<span style='color:{cl}; font-weight:700'>#{k['no']}</span> "
                       f"({k['kuvvet']:.2f}) &nbsp; "
                       f"IF <i>{k['metin']}</i> &nbsp;THEN&nbsp; <b>{k['sonuc_etiketi']}</b></div>",
                       unsafe_allow_html=True)

    with tab5:
        st.markdown("**Farkli Durulastirma Yontemleri**")
        st.caption("Bulanik cikisi tek sayiya cevirmenin farkli yollari. Bu projede weighted centroid kullaniliyor.")
        yon = risk_farkli_yontemlerle(**degerler)
        cols = st.columns(4)
        for col, (ad, deg, aciklama) in zip(cols, [
            ("Weighted Centroid", yon["weighted_centroid"], "Etiket merkezleri kuvvet ile agirliklandirilir"),
            ("Egri Centroid", yon["egri_centroid"], "Aggregate egrinin geometric merkezi"),
            ("Bisector", yon["bisector"], "Egriyi iki esit alana bolen nokta"),
            ("Mean of Maxima", yon["mom"], "En yuksek uyelige sahip noktalarin ortalamasi"),
        ]):
            with col:
                st.metric(ad, f"{deg:.1f}%")
                st.caption(aciklama)

        st.markdown("---")
        st.caption("Bu proje **weighted centroid** kullaniyor. Bu yontem her bulanik kumenin temsil merkezini "
                  f"({', '.join([f'{k}={v:.0f}' for k, v in RISK_TEMSIL.items()])}) kural kuvveti ile carpip "
                  "agirlikli ortalamasini alir. Boylelikle KRITIK kurallari devreye girdiginde risk monoton olarak artar.")

    with tab6:
        st.markdown("**Klasik Esikli Sistem vs Bulanik**")
        kla = klasik_risk_hesapla(**degerler)
        fark = risk_v - kla["risk"]

        col1, col2 = st.columns(2)
        with col1:
            kc = SONUC_RENGI[kategori]
            st.markdown(f"<div class='result-card' style='--c:{kc}'><div class='label'>Bulanik Mantik</div><div class='value'>{risk_v:.1f}%</div><div style='font-size:13px'>{kategori}  •  {len(aktif)} kural</div></div>",
                       unsafe_allow_html=True)
            st.caption("Yumusak gecisli, kurallari kismi olarak birlestirir, surucu yorgunlugunu da hesaba katar.")
        with col2:
            kc = SONUC_RENGI[kla["kategori"]]
            st.markdown(f"<div class='result-card' style='--c:{kc}'><div class='label'>Klasik Esikli</div><div class='value'>{kla['risk']:.1f}%</div><div style='font-size:13px'>{kla['kategori']}</div></div>",
                       unsafe_allow_html=True)
            st.caption("Keskin esiklerle puan toplama: hiz>130: +28, sure>7: +22, vs. Tum-veya-hicbir mantik.")

        st.markdown("---")
        st.markdown(f"**Fark:** {abs(fark):.1f} puan  •  Bulanik {'daha yuksek' if fark > 0 else 'daha dusuk'}")
        st.caption("Klasik sistemde hiz=121 ve hiz=120 arasinda 28 puanlik anlik sicrama olur. Bulanik sistem bu degerler "
                   "arasinda sadece 0.5 puan fark eder. Bu yumusak gecis surucu uyari sistemlerinde kritik onemde.")

    with tab7:
        st.markdown("**10 Hazir Senaryo Karsilastirmasi**")
        @st.cache_data(show_spinner=False)
        def senaryolari_tara():
            rows = []
            for ad, p in HAZIR.items():
                if p is None:
                    continue
                r = risk_hesapla(**p)
                k = klasik_risk_hesapla(**p)
                rows.append({
                    "Senaryo": ad,
                    **{GIRDI_BILGI[g]["baslik"][:8]: v for g, v in p.items()},
                    "Bulanik %": f"{r['risk']:.1f}",
                    "Kategori": r["kategori"],
                    "Oneri": r["oneri_metin"],
                    "Klasik %": f"{k['risk']:.1f}",
                    "Aktif Kural": len(r["aktif_kurallar"]),
                })
            return pd.DataFrame(rows)

        df = senaryolari_tara()
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("CSV olarak indir", csv, file_name="senaryolar.csv", mime="text/csv")

else:
    st.info("Sol panelden degerleri secip HESAPLA butonuna bas (veya otomatik mod acik kalsin).")
