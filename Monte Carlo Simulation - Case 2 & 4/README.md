# Monte Carlo Simulation — Case 2 & Case 4

Proyek ini berisi implementasi simulasi Monte Carlo untuk dua studi kasus:

- **Case 2** — Stock Price Prediction Using Monte Carlo Simulation (Geometric Brownian Motion)
- **Case 4** — Simulate Dice Rolls for a Game of Chance (dua dadu & craps)

Dibuat untuk tugas Modul 3 — Pemodelan Simulasi (Week 6).

---

## 📁 Struktur Folder

```
Monte Carlo - Case 2 & 4/
├── case2_StockPriceSimulation.py       # Script simulasi harga saham BBCA
├── case4_DiceSimulation.py             # Script simulasi dua dadu & craps
├── Bank Central Asia (BBCA) Historical Data.csv   # Data historis harga BBCA
├── case2_bbca_mc.png                   # Output grafik Case 2
├── case4_dice_mc.png                   # Output grafik Case 4
└── README.md                           # File ini
```

---

## 📈 Case 2 — Stock Price Prediction (BBCA)

**Tujuan**: Memodelkan pergerakan harga saham BBCA 30 hari perdagangan ke depan menggunakan model *Geometric Brownian Motion* (GBM), berdasarkan drift dan volatilitas yang diestimasi dari data historis.

**Ringkasan metode**:
- Data historis harga BBCA dibaca dari CSV, dihitung log-return harian
- Drift (μ) dan volatilitas (σ) diestimasi dari log-return
- 10.000 lintasan harga disimulasikan dengan formula:
  `S(t+1) = S(t) · exp[(μ − 0.5σ²)·dt + σ·√dt·Z]`

**Ringkasan hasil**:
| Metrik | Nilai (IDR) |
|---|---|
| Harga awal (S0) | 6.225 |
| Rata-rata harga (hari ke-30) | 5.984 |
| Median harga | 5.976 |
| Persentil 5–95 | 5.272 – 6.734 |
| P(harga naik dari S0) | 28,1% |

**Output**: `case2_bbca_mc.png` — berisi (1) sebaran lintasan harga simulasi, (2) histogram distribusi harga hari ke-30.

**Keterbatasan**: drift diestimasi dari data historis yang relatif sedikit (22 titik), model GBM mengasumsikan volatilitas konstan & return berdistribusi normal, serta tidak memperhitungkan faktor eksternal (berita, kebijakan, jump risk).

---

## 🎲 Case 4 — Dice Rolls & Craps

**Tujuan**: Mengestimasi probabilitas jumlah dua dadu dan probabilitas menang pada permainan craps menggunakan simulasi Monte Carlo, lalu dibandingkan dengan perhitungan teoretis/manual.

**Ringkasan metode**:
- Simulasi 1.000.000 pelemparan dua dadu independen → dihitung frekuensi tiap kemungkinan sum (2–12)
- Simulasi 200.000 game craps mengikuti aturan pass-line (natural, craps, point system)
- Hasil dibandingkan dengan perhitungan probabilitas teoretis (kombinatorik)

**Ringkasan hasil**:
| Metrik | Simulasi | Teoretis |
|---|---|---|
| P(sum = 7) | 16,645% | 16,667% |
| Win rate craps | 49,311% | 49,293% (244/495) |

**Output**: `case4_dice_mc.png` — berisi (1) bar chart perbandingan probabilitas sum simulasi vs teoretis, (2) bar chart hasil menang/kalah craps.

**Kesimpulan**: hasil simulasi sangat mendekati nilai teoretis, selisih < 0,1%, sesuai *Law of Large Numbers*.
